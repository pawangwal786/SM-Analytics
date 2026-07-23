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
    """Create the AsyncEngine connected to the test database."""
    test_engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        echo=False,
    )

    try:
        yield test_engine
    finally:
        await test_engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_schema(
    engine: AsyncEngine,
) -> AsyncGenerator[None, None]:
    """
    Create the database schema before the test session
    and drop it after the session completes.
    """

    # Import models so Base.metadata is fully populated
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
    Create one database connection for each test.
    """
    async with engine.connect() as conn:
        yield conn


@pytest_asyncio.fixture
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncConnection, None]:
    """
    Start an outer transaction for the current test.
    """

    outer_transaction = await connection.begin()

    try:
        yield connection
    finally:
        if outer_transaction.is_active:
            await outer_transaction.rollback()


@pytest_asyncio.fixture
async def db_session(
    transaction: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create an AsyncSession bound to the transactional connection.
    """

    session_factory = async_sessionmaker(
        bind=transaction,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with session_factory() as session:
        yield session
