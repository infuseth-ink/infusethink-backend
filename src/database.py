"""Database configuration and session management."""

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import Settings


@lru_cache
def get_engine():
    """Get cached database engine.

    Returns:
        Engine: SQLAlchemy database engine

    Note:
        Uses lru_cache to create engine only once during app lifetime.
    """
    settings = Settings()  # type: ignore[call-arg]

    # remove in SQLAlchemy 2.1 as this driver bocomes the default for postgresql:// URLs
    url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")

    return create_engine(
        url,
        echo=settings.debug,  # Log SQL queries when debug=True
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=5,  # Number of connections to maintain
        max_overflow=10,  # Max connections beyond pool_size
    )


def get_session():
    """Dependency that provides a database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.scalars(select(Item)).all()
            return items
    """
    with Session(get_engine()) as session:
        yield session
