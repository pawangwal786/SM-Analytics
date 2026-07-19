from contextlib import suppress
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from fastapi import FastAPI, Request
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer

from backend.libs.database.config import DatabaseSettings
from backend.libs.database.engine import create_engine, dispose_engine
from backend.libs.database.health import check_database_health
from backend.libs.database.lifespan import get_database_lifespan
from backend.libs.database.session import create_session_factory, get_session


@pytest.fixture(scope="session")
def postgres_container():
    """Spins up a real PostgreSQL container for integration testing."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_settings(postgres_container):
    """Provides DatabaseSettings linked to the test container."""
    url = postgres_container.get_connection_url()
    # Ensure it uses the asyncpg driver
    if url.startswith("postgresql+psycopg2://"):
        url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")

    return DatabaseSettings(
        database_url=url,
        pool_size=5,
        max_overflow=5,
        pool_timeout=10,
        pool_recycle=1800,
        pool_pre_ping=True,
    )


@pytest_asyncio.fixture(scope="function")
async def db_engine(db_settings):
    """Provides an isolated engine instance for tests."""
    engine = create_engine(db_settings)
    yield engine
    await dispose_engine(engine)


@pytest_asyncio.fixture(scope="function")
async def session_factory(db_engine):
    return create_session_factory(db_engine)


@pytest.mark.asyncio
async def test_engine_creation_and_disposal(db_settings):
    engine = create_engine(db_settings)
    assert engine is not None
    # Dispose to ensure no lingering connections
    await dispose_engine(engine)


@pytest.mark.asyncio
async def test_health_check_healthy(session_factory):
    async with session_factory() as session:
        health = await check_database_health(session)
        assert health["status"] == "up"
        assert "latency_ms" in health
        assert isinstance(health["latency_ms"], float)


@pytest.mark.asyncio
async def test_session_dependency_commits_on_success(session_factory):
    # Mock FastAPI request
    request = MagicMock(spec=Request)
    request.app.state.session_factory = session_factory

    # Create a test table using raw SQL
    async with session_factory() as setup_session:
        await setup_session.execute(
            text("CREATE TABLE IF NOT EXISTS test_commit (id SERIAL PRIMARY KEY, val TEXT)")
        )
        await setup_session.commit()

    # Simulate a successful request using the dependency
    session_gen = get_session(request)
    session = await anext(session_gen)

    await session.execute(text("INSERT INTO test_commit (val) VALUES ('success')"))

    # Complete the generator, which triggers the commit
    with suppress(StopAsyncIteration):
        await anext(session_gen)

    # Verify data was committed
    async with session_factory() as verify_session:
        result = await verify_session.execute(
            text("SELECT count(*) FROM test_commit WHERE val = 'success'")
        )
        count = result.scalar()
        assert count == 1


@pytest.mark.asyncio
async def test_session_dependency_rolls_back_on_error(session_factory):
    request = MagicMock(spec=Request)
    request.app.state.session_factory = session_factory

    # Create table
    async with session_factory() as setup_session:
        await setup_session.execute(
            text("CREATE TABLE IF NOT EXISTS test_rollback (id SERIAL PRIMARY KEY, val TEXT)")
        )
        await setup_session.commit()

    session_gen = get_session(request)
    session = await anext(session_gen)

    await session.execute(text("INSERT INTO test_rollback (val) VALUES ('should_fail')"))

    # Simulate an exception in the route handler
    with pytest.raises(ValueError, match="Route handler failed"):
        await session_gen.athrow(ValueError("Route handler failed"))

    # Verify data was NOT committed
    async with session_factory() as verify_session:
        result = await verify_session.execute(
            text("SELECT count(*) FROM test_rollback WHERE val = 'should_fail'")
        )
        count = result.scalar()
        assert count == 0


@pytest.mark.asyncio
async def test_lifespan_integration(db_settings):
    app = FastAPI()
    lifespan = get_database_lifespan(db_settings)

    async with lifespan(app):
        # Engine and session factory should be attached to app state
        assert hasattr(app.state, "engine")
        assert hasattr(app.state, "session_factory")

        # Verify connectivity using the attached session factory
        async with app.state.session_factory() as session:
            health = await check_database_health(session)
            assert health["status"] == "up"

    # Outside lifespan block, engine is disposed.
    # No direct way to assert 'disposed' via API but this validates no exceptions
    #  are raised during teardown.
