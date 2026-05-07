"""Database configuration and session management."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from wireup import injectable

from .config import Settings


@injectable
def get_engine(settings: Settings) -> AsyncEngine:
    url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")
    return create_async_engine(
        url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


@injectable(lifetime="scoped")
async def get_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with AsyncSession(engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
