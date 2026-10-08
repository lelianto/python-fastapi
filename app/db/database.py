"""SQLAlchemy engine and session helpers."""

from collections.abc import Generator
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session
from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class shared by every ORM model."""


@lru_cache
def get_engine(database_url: str) -> Engine:
    """Create one engine for each database URL."""
    args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=args)


def get_db() -> Generator[Session, None, None]:
    """Provide a session and always close it after the request."""
    with Session(get_engine(get_settings().database_url)) as session:
        yield session


def create_db_and_tables(database_url: str) -> None:
    """Create tables that do not exist yet."""
    from app.models import task  # noqa: F401 - registers the model metadata
    Base.metadata.create_all(get_engine(database_url))
