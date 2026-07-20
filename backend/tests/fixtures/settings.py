import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_test_settings():
    """
    Loads testing environment variables from .env.test before any tests run.
    Ensures that standard runtime code pulls from the correct environment.
    """
    load_dotenv(dotenv_path=".env.test", override=True)
    os.environ["APP_ENV"] = "testing"
