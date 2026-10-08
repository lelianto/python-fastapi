"""Task database operations. Repositories know SQLAlchemy, not HTTP."""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Persist and retrieve tasks using one database session."""
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: TaskCreate) -> Task:
        task = Task(**payload.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def list(self, *, offset: int, limit: int) -> list[Task]:
        query = select(Task).order_by(Task.id).offset(offset).limit(limit)
        return list(self.session.scalars(query))

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def update(self, task: Task, payload: TaskUpdate) -> Task:
        # exclude_unset distinguishes "not sent" from explicitly sent null.
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()
