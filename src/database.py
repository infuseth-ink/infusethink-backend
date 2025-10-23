"""Database configuration and session management."""

from functools import lru_cache

from sqlmodel import Session, create_engine

from .config import get_settings


@lru_cache
def get_engine():
    """Get cached database engine.

    Returns:
        Engine: SQLModel database engine

    Note:
        Uses lru_cache to create engine only once during app lifetime.
    """
    settings = get_settings()

    # SQLAlchemy defaults to psycopg2, but we have psycopg3 installed
    # Explicitly specify the driver for psycopg3
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
        Session: SQLModel database session

    Example:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session
