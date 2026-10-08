"""Task business rules."""

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Raised when a requested task does not exist."""


class TaskService:
    """Coordinate task use cases independently from the HTTP layer."""
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create(self, payload: TaskCreate) -> Task:
        return self.repository.create(payload)

    def list(self, *, offset: int, limit: int) -> list[Task]:
        return self.repository.list(offset=offset, limit=limit)

    def get(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} was not found")
        return task

    def update(self, task_id: int, payload: TaskUpdate) -> Task:
        return self.repository.update(self.get(task_id), payload)

    def delete(self, task_id: int) -> None:
        self.repository.delete(self.get(task_id))
