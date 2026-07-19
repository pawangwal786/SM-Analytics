from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict
from .environment import AppEnv
from .loaders import get_env_file


class BaseSettings(PydanticBaseSettings):
    """
    Base configuration class for all microservices.
    Defines strictly universal properties and handles environment file loading.
    Services should inherit from this and add their specific requirements.
    """

    # Application identity
    app_name: str
    version: str = "0.1.0"

    # Deployment environment
    environment: AppEnv = Field(
        default_factory=lambda: AppEnv.DEVELOPMENT, validation_alias="APP_ENV"
    )
    debug: bool = False

    # Networking
    host: str = "0.0.0.0"
    port: int

    # Observability
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=get_env_file(), env_file_encoding="utf-8", extra="ignore"
    )
