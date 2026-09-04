"""
Acceptance tests for T3 (evals/tasks/T3.md) — task priority, including the
pre-existing-database requirement.

Apparatus, not target — see evals/acceptance/test_T1.py's header for the
same invocation contract (run from inside the trial's taskflow worktree,
so `from src.database import get_session` / `from src.main import app`
resolve). The legacy-database tests additionally need the frozen fixture
at evals/tasks/fixtures/T3_pre_existing_taskflow.db, sha256
2f1034a0edf4ba1a65cfd3a0066153098ad82e67dad5a79bd6813d4d00caf461 (see
evals/protocol.yaml) — the harness copies it to a scratch path before each
trial's legacy-db tests, never runs against the committed original.
"""
import shutil
import pathlib

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app

FIXTURE = pathlib.Path(__file__).resolve().parents[1] / "tasks" / "fixtures" / "T3_pre_existing_taskflow.db"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ── Fresh-database behavior ─────────────────────────────────────────────────


def test_create_without_priority_defaults_to_medium(client: TestClient):
    r = client.post("/tasks/", json={"title": "No priority given"})
    assert r.status_code == 201
    assert r.json()["priority"] == "medium"


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_priority_round_trips_through_create_get_list(client: TestClient, priority):
    r = client.post("/tasks/", json={"title": "Priority test", "priority": priority})
    assert r.status_code == 201
    task_id = r.json()["id"]
    assert r.json()["priority"] == priority

    r_get = client.get(f"/tasks/{task_id}")
    assert r_get.json()["priority"] == priority

    r_list = client.get("/tasks/")
    listed = next(t for t in r_list.json() if t["id"] == task_id)
    assert listed["priority"] == priority


def test_invalid_priority_fails_predictably(client: TestClient):
    r = client.post("/tasks/", json={"title": "Bad priority", "priority": "urgent"})
    assert r.status_code == 422


# ── Pre-existing database (the real point of T3) ────────────────────────────


@pytest.fixture(name="legacy_client")
def legacy_client_fixture(tmp_path, monkeypatch):
    """
    Redirects src.database.engine itself (not just the get_session
    dependency) to a scratch copy of the legacy fixture, then lets the
    real app lifespan run create_db_and_tables() against it — so
    whatever migration logic the trial actually wrote (inside
    create_db_and_tables, or wherever) genuinely executes against a
    pre-existing database, the same as it would in a real deployment.

    This assumes the trial's code still reads/writes through the
    module-level `engine` in src.database, which is the existing
    convention this codebase already uses everywhere (get_session,
    create_db_and_tables) — the task does not ask for a persistence
    layer redesign, so this is not testing an implementation detail
    beyond what the codebase already commits to.
    """
    assert FIXTURE.exists(), f"T3 fixture missing: {FIXTURE}"
    legacy_db = tmp_path / "legacy_taskflow.db"
    shutil.copy(FIXTURE, legacy_db)

    import src.database as database_module
    scratch_engine = create_engine(
        f"sqlite:///{legacy_db}", connect_args={"check_same_thread": False}
    )
    monkeypatch.setattr(database_module, "engine", scratch_engine)

    with TestClient(app) as client:  # __enter__ runs the lifespan -> create_db_and_tables()
        yield client


def test_existing_database_still_readable_after_the_change(legacy_client: TestClient):
    """The real test: a database that predates `priority` must not break."""
    r = legacy_client.get("/tasks/")
    assert r.status_code == 200, (
        "GET /tasks/ crashed against a pre-existing database — "
        "adding a column to the model without migrating the existing "
        "table breaks every pre-existing row."
    )
    tasks = r.json()
    assert len(tasks) == 2, "the fixture's 2 pre-existing rows must still be readable"
    for t in tasks:
        assert t["priority"] == "medium", "pre-existing rows must get the default, not crash or go null"


def test_can_still_create_new_tasks_against_the_legacy_database(legacy_client: TestClient):
    r = legacy_client.post("/tasks/", json={"title": "New task on old DB", "priority": "high"})
    assert r.status_code == 201
    assert r.json()["priority"] == "high"
