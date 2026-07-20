import os
from collections.abc import Generator

import pytest

try:
    from testcontainers.postgres import PostgresContainer
except ImportError:
    PostgresContainer = None


@pytest.fixture(scope="session")
def postgres_container() -> Generator[str | None, None, None]:
    """
    Spins up a PostgreSQL testcontainer if TEST_DATABASE_URL is not set.
    Yields the database URL or None if skipped/failed.
    """
    if os.environ.get("TEST_DATABASE_URL"):
        yield None
        return

    if PostgresContainer is None:
        yield None
        return

    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            # Generate postgresql+asyncpg URL for SQLAlchemy compatibility
            url = postgres.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
            yield url
    except Exception:
        # Gracefully handle cases where Docker daemon isn't running locally
        yield None
