"""
Baseline tests for TaskFlow.

These tests define the baseline behavior before any MetaVibing intervention.
Results from running these against vanilla Claude Code are stored in
evals/baseline/.
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


# ── User tests ────────────────────────────────────────────────────────────────


def test_create_user(client: TestClient):
    response = client.post("/users/", json={"username": "alice", "email": "alice@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["id"] is not None


def test_list_users_empty(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_not_found(client: TestClient):
    response = client.get("/users/999")
    assert response.status_code == 404


# ── Task tests ────────────────────────────────────────────────────────────────


def test_create_task(client: TestClient):
    response = client.post("/tasks/", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False


def test_list_tasks_empty(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_complete_task(client: TestClient):
    r = client.post("/tasks/", json={"title": "Write tests"})
    task_id = r.json()["id"]
    r2 = client.patch(f"/tasks/{task_id}/complete")
    assert r2.status_code == 200
    assert r2.json()["done"] is True


def test_delete_task(client: TestClient):
    r = client.post("/tasks/", json={"title": "Temporary task"})
    task_id = r.json()["id"]
    r2 = client.delete(f"/tasks/{task_id}")
    assert r2.status_code == 204
    r3 = client.get(f"/tasks/{task_id}")
    assert r3.status_code == 404


def test_filter_tasks_by_done(client: TestClient):
    client.post("/tasks/", json={"title": "Pending task"})
    r = client.post("/tasks/", json={"title": "Done task"})
    client.patch(f"/tasks/{r.json()['id']}/complete")

    pending = client.get("/tasks/?done=false").json()
    done = client.get("/tasks/?done=true").json()
    assert len(pending) == 1
    assert len(done) == 1
