"""Integration tests that exercise the API and database together."""

from fastapi.testclient import TestClient


def create_task(client: TestClient, title: str = "Learn FastAPI") -> dict:
    """Test helper that creates a task and returns its JSON body."""
    response = client.post("/api/v1/tasks", json={
        "title": title, "description": "Build a CRUD API"
    })
    assert response.status_code == 201
    return response.json()


def test_create_and_get_task(client: TestClient) -> None:
    created = create_task(client)
    response = client.get(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["completed"] is False


def test_list_tasks_with_pagination(client: TestClient) -> None:
    create_task(client, "First")
    create_task(client, "Second")
    response = client.get("/api/v1/tasks?offset=1&limit=1")
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Second"]


def test_partially_update_task(client: TestClient) -> None:
    task = create_task(client)
    response = client.patch(f"/api/v1/tasks/{task['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == task["title"]
    assert response.json()["completed"] is True


def test_delete_task(client: TestClient) -> None:
    task = create_task(client)
    assert client.delete(f"/api/v1/tasks/{task['id']}").status_code == 204
    assert client.get(f"/api/v1/tasks/{task['id']}").status_code == 404


def test_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task 999 was not found"}


def test_invalid_payload_returns_422(client: TestClient) -> None:
    assert client.post("/api/v1/tasks", json={"title": ""}).status_code == 422


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
