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
    Yields the database URL.
    """
    if os.environ.get("TEST_DATABASE_URL"):
        yield None
        return

    if PostgresContainer is None:
        raise RuntimeError("testcontainers[postgres] is required to run database integration tests.")

    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            # Generate postgresql+asyncpg URL for SQLAlchemy compatibility
            url = postgres.get_connection_url()
            if url.startswith("postgresql+"):
                url = "postgresql+asyncpg://" + url.split("://", maxsplit=1)[1]
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            yield url
    except Exception as error:
        raise RuntimeError("Docker is required to run database integration tests.") from error
