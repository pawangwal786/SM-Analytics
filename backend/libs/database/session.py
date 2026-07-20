import logging
from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

logger = logging.getLogger(__name__)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Creates the SQLAlchemy async_sessionmaker bound to the given engine.
    Configures it with expire_on_commit=False, typical for async usage.
    """
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an isolated AsyncSession per request.
    Enforces the 'One Request -> One Transaction' pattern.
    Commits on success, rolls back on unhandled exceptions.
    """

    session_factory: async_sessionmaker[AsyncSession] | None = getattr(
        request.app.state,
        "session_factory",
        None,
    )

    if session_factory is None:
        raise RuntimeError("Database session_factory not found on app state. Is lifespan configured?")

    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            # Revert any uncommitted changes if an exception occurred during request
            logger.exception("Rolling back database transaction due to unhandled exception")
            await session.rollback()
            raise
