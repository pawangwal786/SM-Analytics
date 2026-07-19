import logging
import sys

from backend.libs.observability.filters.context import ContextInjectionFilter
from backend.libs.observability.formatters.json import JSONFormatter


def configure_logging(service_name: str, environment: str, log_level: str = "INFO"):
    """
    Globally configures standard Python logging to emit structured JSON.
    - Clears existing handlers
    - Sets root log level
    - Attaches JSONFormatter
    - Attaches ContextInjectionFilter for automatic metadata injection
    """
    root_logger = logging.getLogger()

    # Parse log level, defaulting to INFO if invalid
    level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(level)

    # Clear any previously configured handlers (like uvicorn defaults)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure the standard output handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Attach our custom JSON formatter (with automatic redaction)
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    # Attach context injection filter to automatically append request/correlation IDs
    context_filter = ContextInjectionFilter(service=service_name, environment=environment)
    handler.addFilter(context_filter)

    root_logger.addHandler(handler)

    # Suppress verbose loggers from third-party libraries if necessary
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Log startup event
    root_logger.info("Observability layer configured", extra={"event": "startup"})
