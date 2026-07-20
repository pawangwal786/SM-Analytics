from pydantic import Field, PostgresDsn

from backend.libs.settings.core import CoreSettings


class DatabaseSettings(CoreSettings):
    """
    Configuration for the database connection and pooling.
    These settings are intended to be mixed into or initialized by
    service-specific settings.
    """

    database_url: PostgresDsn

    # Pool configurations with production defaults
    pool_size: int = Field(
        default=20,
        description="Number of connections to keep open inside the connection pool",
        validation_alias="DATABASE_POOL_SIZE",
    )
    max_overflow: int = Field(
        default=20,
        description="Number of connections to allow beyond pool_size",
        validation_alias="DATABASE_MAX_OVERFLOW",
    )
    pool_timeout: int = Field(
        default=30,
        description="Seconds to wait before giving up on getting a connection from the pool",
        validation_alias="DATABASE_POOL_TIMEOUT",
    )
    pool_recycle: int = Field(
        default=1800,
        description="Seconds after which a connection is automatically recycled",
        validation_alias="DATABASE_POOL_RECYCLE",
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Enable connection health checks before checking out from the pool",
        validation_alias="DATABASE_POOL_PRE_PING",
    )

    # Connection parameters
    sslmode: str = Field(
        default="prefer",
        description="SSL mode for the database connection (e.g., disable, require, verify-full)",
        validation_alias="DATABASE_SSLMODE",
    )
    statement_timeout: int | None = Field(
        default=None,
        description="Statement timeout in milliseconds",
        validation_alias="DATABASE_STATEMENT_TIMEOUT",
    )
    connect_timeout: int = Field(
        default=10,
        description="Connection timeout in seconds",
        validation_alias="DATABASE_CONNECT_TIMEOUT",
    )
    application_name: str = Field(
        default="sm-analytics",
        description="Application name reported to PostgreSQL",
        validation_alias="DATABASE_APPLICATION_NAME",
    )
