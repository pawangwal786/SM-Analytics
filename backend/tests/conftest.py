# backend/tests/conftest.py
"""
Global pytest configuration and fixture registry.
All actual fixtures are defined in the backend.tests.fixtures module.
"""

pytest_plugins = [
    "backend.tests.fixtures.settings",
    "backend.tests.fixtures.containers",
    "backend.tests.fixtures.database",
    "backend.tests.fixtures.engine",
]
