import os
import sys
from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn, SecretStr

# Ensure backend directory is in the path to allow imports, since we
# aren't using an installed package yet.
# In a real deployed environment with a workspace, this would be handled by Python packaging.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from backend.libs.settings.base import BaseSettings


class AuthSettings(BaseSettings):
    """Configuration for the Auth service."""

    # Required overrides (will fail fast if not present in environment)
    app_name: str = "sm-auth-service"
    port: int = 8001

    # Auth specific
    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_ttl: int = 3600
    refresh_token_ttl: int = 86400

    # Databases
    database_url: PostgresDsn
    redis_url: RedisDsn


@lru_cache
def get_settings() -> AuthSettings:
    """Dependency injection provider for AuthSettings."""
    return AuthSettings()
