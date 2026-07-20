import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from backend.libs.database.config import DatabaseSettings
from backend.libs.database.engine import create_engine, dispose_engine
from backend.libs.database.session import create_session_factory

logger = logging.getLogger(__name__)


def get_database_lifespan(
    settings: DatabaseSettings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Initializing database infrastructure")

        engine = create_engine(settings)
        session_factory = create_session_factory(engine)

        app.state.engine = engine
        app.state.session_factory = session_factory

        try:
            yield
        finally:
            logger.info("Disposing database infrastructure")
            await dispose_engine(engine)

    return lifespan
