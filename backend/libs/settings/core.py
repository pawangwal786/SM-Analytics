from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from .environment import AppEnv
from .loaders import get_env_file


class CoreSettings(PydanticBaseSettings):
    """
    Universal configuration class for all services, workers, and tools.
    Defines strictly universal properties (environment, observability)
    and handles environment file loading.
    No application identity or networking configuration should be placed here.
    """

    # Deployment environment
    environment: AppEnv = Field(default_factory=lambda: AppEnv.DEVELOPMENT, validation_alias="APP_ENV")
    debug: bool = False

    # Observability
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=get_env_file(), env_file_encoding="utf-8", extra="ignore")
