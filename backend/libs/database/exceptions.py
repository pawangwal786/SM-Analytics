class DatabaseError(Exception):
    """Base class for all database exceptions in the library."""

    pass


class ConfigurationError(DatabaseError):
    """Raised when the database configuration is invalid."""

    pass


class ConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""

    pass
