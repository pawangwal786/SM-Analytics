from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.libs.database.base import Base


@pytest_asyncio.fixture(scope="session")
async def engine(database_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """Creates the AsyncEngine connected to the test database."""
    test_engine = create_async_engine(database_url, pool_pre_ping=True, echo=False)
    yield test_engine
    await test_engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Creates the session factory bound to the test engine."""
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_schema(engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """
    Creates all tables in the test database before the test session starts,
    and drops them after it finishes.
    """
    # Make sure all models are imported so Base.metadata is fully populated
    import backend.services.auth.app.models  # noqa: F401
    import backend.services.users.app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an isolated AsyncSession per test.
    Wraps the test inside a savepoint (nested transaction) and rolls it back after the test completes.
    This provides fast test isolation without re-creating tables.
    """

    async with session_factory() as session, session.begin():
        # Start a nested savepoint
        nested = await session.begin_nested()

        yield session

        # Rollback the savepoint when test completes
        await nested.rollback()
