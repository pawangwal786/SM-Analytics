from pydantic import Field, PostgresDsn

from backend.libs.settings.base import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Configuration for the database connection and pooling.
    These settings are intended to be mixed into or initialized by
    service-specific settings.
    """

    database_url: PostgresDsn

    # Pool configurations with production defaults
    pool_size: int = Field(
        default=20, description="Number of connections to keep open inside the connection pool"
    )
    max_overflow: int = Field(
        default=20, description="Number of connections to allow beyond pool_size"
    )
    pool_timeout: int = Field(
        default=30,
        description="Seconds to wait before giving up on getting a connection from the pool",
    )
    pool_recycle: int = Field(
        default=1800, description="Seconds after which a connection is automatically recycled"
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Enable connection health checks before checking out from the pool",
    )

    # Connection parameters
    sslmode: str = Field(
        default="prefer",
        description="SSL mode for the database connection (e.g., disable, require, verify-full)",
    )
    statement_timeout: int | None = Field(
        default=None, description="Statement timeout in milliseconds"
    )
    connect_timeout: int = Field(default=10, description="Connection timeout in seconds")
    application_name: str = Field(
        default="sm-analytics", description="Application name reported to PostgreSQL"
    )
