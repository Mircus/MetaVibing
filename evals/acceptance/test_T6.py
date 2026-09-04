"""
Acceptance tests for T6 (evals/tasks/T6.md) — GET /stats/tasks.

Apparatus, not target — see evals/acceptance/test_T1.py's header for the
invocation contract.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app


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


def test_stats_on_empty_database(client: TestClient):
    r = client.get("/stats/tasks")
    assert r.status_code == 200
    body = r.json()
    assert body == {"total": 0, "pending": 0, "completed": 0}


def test_stats_counts_are_correct_and_consistent(client: TestClient):
    ids = []
    for i in range(5):
        r = client.post("/tasks/", json={"title": f"Task {i}"})
        ids.append(r.json()["id"])
    for tid in ids[:2]:
        client.patch(f"/tasks/{tid}/complete")

    r = client.get("/stats/tasks")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"total", "pending", "completed"}
    assert body["total"] == 5
    assert body["completed"] == 2
    assert body["pending"] == 3
    assert body["pending"] + body["completed"] == body["total"]


# ── Regression: every pre-existing endpoint must be untouched ──────────────


def test_existing_endpoints_unchanged_create_task(client: TestClient):
    r = client.post("/tasks/", json={"title": "Buy milk"})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"
    assert r.json()["done"] is False


def test_existing_endpoints_unchanged_list_tasks_empty(client: TestClient):
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert r.json() == []


def test_existing_endpoints_unchanged_complete_and_delete(client: TestClient):
    r = client.post("/tasks/", json={"title": "Write tests"})
    task_id = r.json()["id"]

    r2 = client.patch(f"/tasks/{task_id}/complete")
    assert r2.status_code == 200
    assert r2.json()["done"] is True

    r3 = client.delete(f"/tasks/{task_id}")
    assert r3.status_code == 204

    r4 = client.get(f"/tasks/{task_id}")
    assert r4.status_code == 404


def test_existing_endpoints_unchanged_users(client: TestClient):
    r = client.post("/users/", json={"username": "alice", "email": "alice@example.com"})
    assert r.status_code == 201
    r2 = client.get("/users/")
    assert r2.status_code == 200
    r3 = client.get("/users/999")
    assert r3.status_code == 404
