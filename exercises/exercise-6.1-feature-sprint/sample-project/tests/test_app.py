"""Tests for the Task Management API."""

import pytest

from app import create_app
from models import db


@pytest.fixture()
def app():
    """Create a test application instance."""
    app = create_app(testing=True)
    yield app


@pytest.fixture()
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture()
def sample_task(client):
    """Create and return a sample task."""
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Add unit tests for the API",
            "priority": "high",
        },
    )
    return response.get_json()["data"]


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------


class TestListTasks:
    """Tests for GET /tasks."""

    def test_list_tasks_empty(self, client):
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.get_json()
        assert data["data"] == []

    def test_list_tasks_returns_all(self, client):
        client.post("/tasks", json={"title": "Task 1"})
        client.post("/tasks", json={"title": "Task 2"})

        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 2

    def test_list_tasks_filter_by_status(self, client):
        client.post("/tasks", json={"title": "Pending task", "status": "pending"})
        client.post("/tasks", json={"title": "Done task", "status": "done"})

        response = client.get("/tasks?status=pending")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["status"] == "pending"

    def test_list_tasks_invalid_status_filter(self, client):
        response = client.get("/tasks?status=invalid")
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# GET /tasks/<id>
# ---------------------------------------------------------------------------


class TestGetTask:
    """Tests for GET /tasks/<id>."""

    def test_get_existing_task(self, client, sample_task):
        response = client.get(f"/tasks/{sample_task['id']}")
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert data["title"] == "Write tests"
        assert data["priority"] == "high"

    def test_get_nonexistent_task(self, client):
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "error" in response.get_json()


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------


class TestCreateTask:
    """Tests for POST /tasks."""

    def test_create_task_minimal(self, client):
        response = client.post("/tasks", json={"title": "New task"})
        assert response.status_code == 201
        data = response.get_json()["data"]
        assert data["title"] == "New task"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"

    def test_create_task_full(self, client):
        response = client.post(
            "/tasks",
            json={
                "title": "Full task",
                "description": "A complete task",
                "status": "in_progress",
                "priority": "low",
                "due_date": "2026-12-31",
            },
        )
        assert response.status_code == 201
        data = response.get_json()["data"]
        assert data["title"] == "Full task"
        assert data["status"] == "in_progress"
        assert data["priority"] == "low"
        assert data["due_date"] == "2026-12-31"

    def test_create_task_missing_title(self, client):
        response = client.post("/tasks", json={"description": "No title"})
        assert response.status_code == 400

    def test_create_task_empty_title(self, client):
        response = client.post("/tasks", json={"title": "   "})
        assert response.status_code == 400

    def test_create_task_invalid_status(self, client):
        response = client.post(
            "/tasks", json={"title": "Bad status", "status": "invalid"}
        )
        assert response.status_code == 400

    def test_create_task_invalid_priority(self, client):
        response = client.post(
            "/tasks", json={"title": "Bad priority", "priority": "urgent"}
        )
        assert response.status_code == 400

    def test_create_task_invalid_due_date(self, client):
        response = client.post(
            "/tasks", json={"title": "Bad date", "due_date": "not-a-date"}
        )
        assert response.status_code == 400

    def test_create_task_no_json_body(self, client):
        response = client.post(
            "/tasks", data="not json", content_type="application/json"
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# PATCH /tasks/<id>
# ---------------------------------------------------------------------------


class TestUpdateTask:
    """Tests for PATCH /tasks/<id>."""

    def test_update_title(self, client, sample_task):
        response = client.patch(
            f"/tasks/{sample_task['id']}",
            json={"title": "Updated title"},
        )
        assert response.status_code == 200
        assert response.get_json()["data"]["title"] == "Updated title"

    def test_update_status(self, client, sample_task):
        response = client.patch(
            f"/tasks/{sample_task['id']}",
            json={"status": "done"},
        )
        assert response.status_code == 200
        assert response.get_json()["data"]["status"] == "done"

    def test_update_nonexistent_task(self, client):
        response = client.patch("/tasks/999", json={"title": "Nope"})
        assert response.status_code == 404

    def test_update_invalid_status(self, client, sample_task):
        response = client.patch(
            f"/tasks/{sample_task['id']}",
            json={"status": "invalid"},
        )
        assert response.status_code == 400

    def test_update_empty_title(self, client, sample_task):
        response = client.patch(
            f"/tasks/{sample_task['id']}",
            json={"title": ""},
        )
        assert response.status_code == 400

    def test_update_clear_due_date(self, client):
        create = client.post(
            "/tasks", json={"title": "Dated", "due_date": "2026-06-15"}
        )
        task_id = create.get_json()["data"]["id"]

        response = client.patch(f"/tasks/{task_id}", json={"due_date": None})
        assert response.status_code == 200
        assert response.get_json()["data"]["due_date"] is None
