import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from pydantic import ValidationError
except ImportError:
    print("Pydantic not installed. Please install 'pydantic' and 'pydantic-settings'.")
    sys.exit(1)

from backend.libs.settings.environment import AppEnv
from backend.libs.settings.exceptions import ConfigurationError
from backend.libs.settings.loaders import get_env_file
from backend.libs.settings.service import ServiceSettings


def main():
    print("Running config verifications...")

    # 1. Test invalid APP_ENV
    os.environ["APP_ENV"] = "invalid_env"
    try:
        get_env_file()
        print("FAIL: get_env_file should have raised ConfigurationError")
        sys.exit(1)
    except ConfigurationError:
        print("PASS: get_env_file rejected invalid environment")

    # 2. Test valid APP_ENV defaults
    if "APP_ENV" in os.environ:
        del os.environ["APP_ENV"]
    assert get_env_file() == ".env.development"
    print("PASS: get_env_file defaults to development")

    # 3. Test ServiceSettings missing required fields
    os.environ["APP_ENV"] = "testing"
    # Ensure app_name is not in env
    if "APP_NAME" in os.environ:
        del os.environ["APP_NAME"]
    if "APP_PORT" in os.environ:
        del os.environ["APP_PORT"]

    # Create empty .env.testing to avoid FileNotFoundError if ServiceSettings looks for it strictly
    # Actually pydantic-settings just ignores missing env files by default
    # unless specified otherwise.

    try:
        ServiceSettings()
        print("FAIL: ServiceSettings should have raised ValidationError for missing required fields")
        sys.exit(1)
    except ValidationError:
        print("PASS: ServiceSettings raised ValidationError for missing required fields")

    # 4. Test ServiceSettings with valid fields
    os.environ["APP_NAME"] = "test-service"
    os.environ["APP_PORT"] = "8080"

    settings = ServiceSettings()
    assert settings.app_name == "test-service"
    assert settings.app_port == 8080
    assert settings.environment == AppEnv.TESTING
    print("PASS: ServiceSettings instantiated successfully with environment variables")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
