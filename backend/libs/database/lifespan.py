import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.libs.database.config import DatabaseSettings
from backend.libs.database.engine import create_engine, dispose_engine
from backend.libs.database.session import create_session_factory

logger = logging.getLogger(__name__)


def get_database_lifespan(
    settings: DatabaseSettings,
) -> Callable[[FastAPI], AsyncGenerator[None, None]]:
    """
    Returns an async context manager suitable for FastAPI's lifespan.
    It manages the creation and disposal of the async database engine.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting up database infrastructure...")
        engine = create_engine(settings)
        session_factory = create_session_factory(engine)

        # Attach to app state for dependency injection
        app.state.engine = engine
        app.state.session_factory = session_factory

        yield

        logger.info("Shutting down database infrastructure...")
        await dispose_engine(engine)

    return lifespan
