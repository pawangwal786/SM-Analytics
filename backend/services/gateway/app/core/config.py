import os
from functools import lru_cache
from typing import List
import sys

# Ensure backend directory is in the path to allow imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from libs.settings.base import BaseSettings


class GatewaySettings(BaseSettings):
    """Configuration for the Gateway service."""

    app_name: str = "sm-gateway-service"
    port: int = 8000

    # Gateway specific
    cors_origins: List[str] = ["*"]


@lru_cache()
def get_settings() -> GatewaySettings:
    """Dependency injection provider for GatewaySettings."""
    return GatewaySettings()
