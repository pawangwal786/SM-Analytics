import os
from functools import lru_cache
from pydantic import PostgresDsn, RedisDsn
import sys

# Ensure backend directory is in the path to allow imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from libs.settings.base import BaseSettings


class UserSettings(BaseSettings):
    """Configuration for the Users service."""

    app_name: str = "sm-users-service"
    port: int = 8002

    # Databases
    database_url: PostgresDsn
    redis_url: RedisDsn


@lru_cache()
def get_settings() -> UserSettings:
    """Dependency injection provider for UserSettings."""
    return UserSettings()
