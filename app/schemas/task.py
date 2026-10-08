"""Validation schemas for task API input and output."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Fields accepted when a client creates a task."""
    title: str = Field(min_length=1, max_length=200, examples=["Learn FastAPI"])
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = False


class TaskUpdate(BaseModel):
    """Optional fields accepted for a partial update."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None


class TaskRead(BaseModel):
    """Public task representation returned to clients."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
