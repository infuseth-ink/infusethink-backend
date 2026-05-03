"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from wireup import injectable


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string (required)
        debug: Enable debug mode with SQL query logging (default: False)
        git_sha: Git commit SHA for deployment tracking (default: "unknown")

    Example .env file:
        DATABASE_URL=postgresql://user:password@localhost:5432/dbname
        DEBUG=false
        GIT_SHA=abc1234
    """

    database_url: str
    """PostgreSQL connection string, e.g. postgresql+psycopg://user:password@localhost:5432/dbname"""

    debug: bool = False
    """Enable debug mode with SQL query logging (default: False)"""

    git_sha: str | None = None
    """Current Git SHA of the deployed code.  Always available in remote environments,
    but would almost always be None in local development unless explicitly set.

    Helps determine if latest code is deployed and can rule out old code still being served.
    """

    model_config = SettingsConfigDict(env_file=".env")


@injectable
def settings_factory() -> Settings:
    """Create the Settings instance from environment variables, necessary since Wireup thinks the
    settings class needs database_url, debug, etc. as injectables, but we want to load those from
    environment variables using Pydantic's BaseSettings."""
    return Settings()  # type: ignore[call-arg]
