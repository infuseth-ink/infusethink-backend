"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string (required)
        debug: Enable debug mode with SQL query logging (default: False)

    Example .env file:
        DATABASE_URL=postgresql://user:password@localhost:5432/dbname
        DEBUG=false
    """

    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings

    Note:
        Uses lru_cache to create settings only once during app lifetime.
        This is FastAPI's recommended pattern for settings management.
    """
    return Settings()  # type: ignore[call-arg]
