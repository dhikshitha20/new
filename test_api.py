import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

# Use an in-memory SQLite DB for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def register_and_login(client, username="testuser", password="testpass123"):
    client.post("/auth/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": password,
    })
    resp = client.post("/auth/login", json={"username": username, "password": password})
    return resp.json()["access_token"]


# ── Auth Tests ────────────────────────────────────────────────────────────────

def test_register(client):
    resp = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",
    })
    assert resp.status_code == 201
    assert resp.json()["username"] == "alice"


def test_register_duplicate_username(client):
    data = {"username": "bob", "email": "bob@example.com", "password": "secret123"}
    client.post("/auth/register", json=data)
    resp = client.post("/auth/register", json={**data, "email": "bob2@example.com"})
    assert resp.status_code == 400


def test_login(client):
    client.post("/auth/register", json={
        "username": "carol",
        "email": "carol@example.com",
        "password": "secret123",
    })
    resp = client.post("/auth/login", json={"username": "carol", "password": "secret123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "dave",
        "email": "dave@example.com",
        "password": "secret123",
    })
    resp = client.post("/auth/login", json={"username": "dave", "password": "wrong"})
    assert resp.status_code == 401


# ── Task Tests ────────────────────────────────────────────────────────────────

def test_create_task(client):
    token = register_and_login(client)
    resp = client.post("/tasks", json={"title": "Buy milk", "description": "2%"},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "Buy milk"


def test_list_tasks(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/tasks", json={"title": "Task 1"}, headers=headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=headers)
    resp = client.get("/tasks", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


def test_get_task(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "Read book"}, headers=headers).json()
    resp = client.get(f"/tasks/{created['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_update_task(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "Old title"}, headers=headers).json()
    resp = client.put(f"/tasks/{created['id']}", json={"title": "New title", "completed": True},
                      headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "New title"
    assert resp.json()["completed"] is True


def test_delete_task(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/tasks", json={"title": "Temp task"}, headers=headers).json()
    resp = client.delete(f"/tasks/{created['id']}", headers=headers)
    assert resp.status_code == 204


def test_filter_completed_tasks(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    t1 = client.post("/tasks", json={"title": "Done"}, headers=headers).json()
    client.post("/tasks", json={"title": "Pending"}, headers=headers)
    client.put(f"/tasks/{t1['id']}", json={"completed": True}, headers=headers)

    resp = client.get("/tasks?completed=true", headers=headers)
    assert resp.json()["total"] == 1

    resp2 = client.get("/tasks?completed=false", headers=headers)
    assert resp2.json()["total"] == 1


def test_cannot_access_other_users_task(client):
    token1 = register_and_login(client, "user1", "pass1234")
    token2 = register_and_login(client, "user2", "pass1234")
    task = client.post("/tasks", json={"title": "Private"},
                       headers={"Authorization": f"Bearer {token1}"}).json()
    resp = client.get(f"/tasks/{task['id']}", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 404


def test_pagination(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    for i in range(15):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

    resp = client.get("/tasks?page=1&page_size=10", headers=headers)
    data = resp.json()
    assert data["total"] == 15
    assert len(data["tasks"]) == 10

    resp2 = client.get("/tasks?page=2&page_size=10", headers=headers)
    assert len(resp2.json()["tasks"]) == 5
