import pytest
from pydantic import ValidationError

from backend.libs.settings.core import CoreSettings
from backend.libs.settings.environment import AppEnv
from backend.libs.settings.exceptions import ConfigurationError
from backend.libs.settings.loaders import get_env_file
from backend.libs.settings.service import ServiceSettings


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


def test_core_settings_defaults(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")

    settings = CoreSettings()
    assert settings.environment == AppEnv.TESTING
    assert settings.log_level == "INFO"
    assert settings.debug is False


def test_service_settings_missing_required(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    # Missing required field `app_name` should raise validation error
    with pytest.raises(ValidationError) as exc:
        ServiceSettings()

    errors = exc.value.errors()
    assert any(e["loc"] == ("app_name",) for e in errors)


def test_service_settings_success(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("APP_PORT", "8080")

    settings = ServiceSettings()
    assert settings.app_name == "test-app"
    assert settings.app_port == 8080
    assert settings.environment == AppEnv.TESTING
    assert settings.log_level == "INFO"
