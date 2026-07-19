import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.libs.database.config import DatabaseSettings

logger = logging.getLogger(__name__)


def create_engine(settings: DatabaseSettings, **kwargs: Any) -> AsyncEngine:
    """
    Creates and returns an AsyncEngine based on the provided configuration.
    Configures connection pooling and connection arguments (timeout, sslmode).
    """
    connect_args: dict[str, Any] = {
        "server_settings": {"application_name": settings.application_name},
        "command_timeout": settings.connect_timeout,
        "timeout": settings.connect_timeout,
    }

    if settings.statement_timeout:
        # statement_timeout is set per connection upon establishment
        connect_args["server_settings"]["statement_timeout"] = str(settings.statement_timeout)

    # SSL Mode handling for asyncpg
    if settings.sslmode and settings.sslmode != "disable":
        connect_args["ssl"] = settings.sslmode

    # Ensure URL is asyncpg
    url = str(settings.database_url)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    logger.info(
        "Initializing async database engine",
        extra={
            "pool_size": settings.pool_size,
            "max_overflow": settings.max_overflow,
            "pool_pre_ping": settings.pool_pre_ping,
        },
    )

    return create_async_engine(
        url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
        pool_pre_ping=settings.pool_pre_ping,
        connect_args=connect_args,
        **kwargs,
    )


async def dispose_engine(engine: AsyncEngine) -> None:
    """
    Safely disposes of the database engine and its connection pool.
    """
    if engine:
        logger.info("Disposing async database engine and closing connection pools")
        await engine.dispose()
