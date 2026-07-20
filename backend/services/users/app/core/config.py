import os
import sys
from functools import lru_cache

# Ensure backend directory is in the path to allow imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from backend.libs.cache.config import RedisSettings
from backend.libs.database.config import DatabaseSettings
from backend.libs.settings.service import ServiceSettings


class UserSettings(DatabaseSettings, RedisSettings, ServiceSettings):
    """Configuration for the Users service."""

    app_name: str = "sm-users-service"
    app_port: int = 8002


@lru_cache
def get_settings() -> UserSettings:
    """Dependency injection provider for UserSettings."""
    return UserSettings()
