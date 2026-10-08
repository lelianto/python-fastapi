"""Shared pytest fixtures with a fresh temporary database per test."""

from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.config import Settings
from app.db.database import Base, get_db
from app.main import create_app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Return a client connected to an isolated SQLite database."""
    # StaticPool makes every session share the same in-memory SQLite database.
    # It is fast, isolated, and avoids creating or locking test files.
    database_url = "sqlite://"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app = create_app(Settings(database_url=database_url))
    app.dependency_overrides[get_db] = override_get_db
    # Tables already exist, so this fixture does not need to run app lifespan.
    # Avoiding the context manager also keeps this compatible across Starlette
    # and AnyIO versions while preserving real ASGI request handling.
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    engine.dispose()
