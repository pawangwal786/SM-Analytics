from pydantic import RedisDsn

from backend.libs.settings.core import CoreSettings


class RedisSettings(CoreSettings):
    """
    Configuration for Redis connection.
    These settings are intended to be mixed into or initialized by
    service-specific settings.
    """

    redis_url: RedisDsn
