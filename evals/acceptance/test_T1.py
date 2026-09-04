"""
Acceptance tests for T1 (evals/tasks/T1.md) — pagination on GET /tasks/.

Apparatus, not target: this file is part of the frozen evaluation apparatus
(see evals/protocol.yaml). It is run by the trial harness AFTER Claude's
first submission for a T1 trial, against the trial's own src/. It is not
merely "not handed to Claude" — it must live in the evaluator_checkout,
physically outside whatever filesystem tree Claude's trial session can
read (see evals/protocol.yaml's acceptance_test_isolation), since being in
the same repo Claude can grep is not isolation.

Invocation contract: run with examples/taskflow/ as the import root, same
as examples/taskflow/tests/test_tasks.py (i.e. `from src.database import
get_session`, `from src.main import app` must resolve) — the harness runs
this from inside the trial's taskflow worktree, not from evals/.
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


def _create_tasks(client: TestClient, n: int, done: bool = False):
    ids = []
    for i in range(n):
        r = client.post("/tasks/", json={"title": f"Task {i}"})
        assert r.status_code == 201
        ids.append(r.json()["id"])
    if done:
        for tid in ids:
            client.patch(f"/tasks/{tid}/complete")
    return ids


def test_no_pagination_params_still_works(client: TestClient):
    """Old callers with no pagination params at all must not break."""
    _create_tasks(client, 5)
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 5


def test_response_shape_is_still_a_bare_list(client: TestClient):
    """No new wrapper object (no {"items": ...} / {"total": ...})."""
    _create_tasks(client, 3)
    r = client.get("/tasks/?limit=2&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list), "response must stay a bare JSON array"
    assert len(body) == 2


def test_default_limit_is_20(client: TestClient):
    _create_tasks(client, 25)
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert len(r.json()) == 20


def test_limit_and_offset_page_correctly(client: TestClient):
    ids = _create_tasks(client, 10)
    page1 = client.get("/tasks/?limit=4&offset=0").json()
    page2 = client.get("/tasks/?limit=4&offset=4").json()
    page3 = client.get("/tasks/?limit=4&offset=8").json()

    assert [t["id"] for t in page1] == ids[0:4]
    assert [t["id"] for t in page2] == ids[4:8]
    assert [t["id"] for t in page3] == ids[8:10]


def test_pagination_composes_with_done_filter(client: TestClient):
    pending_ids = _create_tasks(client, 6, done=False)
    done_ids = _create_tasks(client, 6, done=True)

    r = client.get("/tasks/?done=true&limit=3&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 3
    assert all(t["id"] in done_ids for t in body)

    r2 = client.get("/tasks/?done=false&limit=3&offset=3")
    assert r2.status_code == 200
    body2 = r2.json()
    assert all(t["id"] in pending_ids for t in body2)


@pytest.mark.parametrize("limit", [0, -1, 101, 1000])
def test_out_of_bounds_limit_is_422(client: TestClient, limit):
    r = client.get(f"/tasks/?limit={limit}")
    assert r.status_code == 422


def test_negative_offset_is_422(client: TestClient):
    r = client.get("/tasks/?offset=-1")
    assert r.status_code == 422


def test_limit_boundaries_are_accepted(client: TestClient):
    _create_tasks(client, 5)
    assert client.get("/tasks/?limit=1").status_code == 200
    assert client.get("/tasks/?limit=100").status_code == 200
