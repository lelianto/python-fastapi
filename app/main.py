"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.db.database import create_db_and_tables


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an app instance; a factory keeps tests isolated and configurable."""
    current_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        # Convenient for learning. Production apps normally use Alembic migrations.
        create_db_and_tables(current_settings.database_url)
        yield

    application = FastAPI(
        title=current_settings.app_name,
        version="1.0.0",
        description="A small, layered CRUD API for learning FastAPI.",
        lifespan=lifespan,
    )
    application.include_router(api_router, prefix=current_settings.api_prefix)

    @application.get("/health", tags=["health"], summary="Check API health")
    def health_check() -> dict[str, str]:
        """Return a lightweight response without accessing the database."""
        return {"status": "ok"}

    return application
