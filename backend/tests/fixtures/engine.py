from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.libs.database.base import Base


@pytest_asyncio.fixture(scope="session")
async def engine(database_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """Creates the AsyncEngine connected to the test database."""
    test_engine = create_async_engine(database_url, pool_pre_ping=True, echo=False)
    yield test_engine
    await test_engine.dispose()


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
async def connection(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncConnection, None]:
    """
    Creates a dedicated database connection for each test.
    """
    async with engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncConnection, None]:
    """
    Starts an outer database transaction for each test and rolls it back
    after the test completes.
    """
    outer_transaction = await connection.begin()

    try:
        yield connection
    finally:
        await outer_transaction.rollback()


@pytest_asyncio.fixture
async def db_session(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an AsyncSession bound to the per-test connection.

    The fixture does not own the transaction lifecycle. Transaction
    management is handled by the outer transaction fixture.
    """
    session_factory = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with session_factory() as session:
        yield session
