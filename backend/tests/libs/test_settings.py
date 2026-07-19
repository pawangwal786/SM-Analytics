import pytest
from pydantic import ValidationError

from libs.settings.environment import AppEnv
from libs.settings.exceptions import ConfigurationError
from libs.settings.loaders import get_env_file
from libs.settings.base import BaseSettings


def test_app_env_enum():
    assert AppEnv("development") == AppEnv.DEVELOPMENT
    assert AppEnv("testing") == AppEnv.TESTING
    assert AppEnv("production") == AppEnv.PRODUCTION

    with pytest.raises(ValueError):
        AppEnv("staging")


def test_get_env_file_default(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    assert get_env_file() == ".env.development"


def test_get_env_file_testing(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    assert get_env_file() == ".env.testing"


def test_get_env_file_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    assert get_env_file() == ".env.production"


def test_get_env_file_invalid(monkeypatch):
    monkeypatch.setenv("APP_ENV", "staging")
    with pytest.raises(ConfigurationError) as exc:
        get_env_file()
    assert "Invalid APP_ENV: 'staging'" in str(exc.value)


def test_base_settings_defaults(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    # Missing required field `app_name` and `port` should raise validation error
    with pytest.raises(ValidationError) as exc:
        BaseSettings()

    errors = exc.value.errors()
    assert any(e["loc"] == ("app_name",) for e in errors)
    assert any(e["loc"] == ("port",) for e in errors)


def test_base_settings_success(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("PORT", "8080")

    settings = BaseSettings()
    assert settings.app_name == "test-app"
    assert settings.port == 8080
    assert settings.environment == AppEnv.TESTING
    assert settings.log_level == "INFO"
