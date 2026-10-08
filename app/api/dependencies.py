"""Reusable FastAPI dependency providers."""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.task import TaskRepository
from app.services.task import TaskService

DatabaseSession = Annotated[Session, Depends(get_db)]


def get_task_service(session: DatabaseSession) -> TaskService:
    """Build a task service for the current request."""
    return TaskService(TaskRepository(session))


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]
