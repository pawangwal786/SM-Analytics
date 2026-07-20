import os
import sys
from functools import lru_cache

# Ensure backend directory is in the path to allow imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from backend.libs.settings.service import ServiceSettings


class GatewaySettings(ServiceSettings):
    """Configuration for the Gateway service."""

    app_name: str = "sm-gateway-service"
    app_port: int = 8000

    # Gateway specific
    cors_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> GatewaySettings:
    """Dependency injection provider for GatewaySettings."""
    return GatewaySettings()
