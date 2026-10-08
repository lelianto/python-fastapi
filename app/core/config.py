"""Application settings loaded from environment variables."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings; each value can be overridden by an environment variable."""

    app_name: str = "Task CRUD API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./tasks.db"
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")


@lru_cache
def get_settings() -> Settings:
    """Parse and cache settings once per process."""
    return Settings()
