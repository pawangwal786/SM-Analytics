import os

import pytest


@pytest.fixture(scope="session")
def database_url(postgres_container: str | None) -> str:
    """
    Resolves the canonical testing database URL.
    Priority: TEST_DATABASE_URL environment variable -> testcontainers -> error.
    """

    # 1. Check for explicit environment variable (CI, Docker Compose, local config)
    env_url = os.environ.get("TEST_DATABASE_URL")
    if env_url:
        if not env_url.startswith("postgresql+asyncpg://"):
            raise RuntimeError("TEST_DATABASE_URL must use the asyncpg SQLAlchemy dialect.")
        return env_url

    # 2. Fall back to automatically provisioned testcontainer
    if postgres_container:
        return postgres_container

    # 3. Fail fast when no database is available for integration tests.
    raise RuntimeError("No TEST_DATABASE_URL was provided and no test database could be started.")
