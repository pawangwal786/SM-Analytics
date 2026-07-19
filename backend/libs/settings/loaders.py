import os
from .environment import AppEnv


def get_env_file() -> str:
    """
    Detects the current APP_ENV and returns the corresponding .env file name.
    Fails fast if APP_ENV is invalid or not set.
    """
    env = os.getenv("APP_ENV", "development").lower()

    try:
        app_env = AppEnv(env)
    except ValueError:
        from .exceptions import ConfigurationError

        valid_envs = [e.value for e in AppEnv]
        raise ConfigurationError(
            f"Invalid APP_ENV: '{env}'. Must be one of {valid_envs}."
        )

    if app_env == AppEnv.PRODUCTION:
        return ".env.production"
    elif app_env == AppEnv.TESTING:
        return ".env.testing"

    return ".env.development"
