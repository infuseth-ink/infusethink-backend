"""Database configuration and session management."""

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from wireup import injectable

from .config import Settings


@injectable
def get_engine(settings: Settings) -> Engine:
    # remove in SQLAlchemy 2.1 as this driver becomes the default for postgresql:// URLs
    url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")
    return create_engine(
        url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


@injectable(lifetime="scoped")
def get_session(engine: Engine) -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
