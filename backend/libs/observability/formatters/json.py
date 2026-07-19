import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from ..filters.redaction import Redactor


class JSONFormatter(logging.Formatter):
    """
    JSON Formatter that emits structured logs in a consistent machine-readable schema.
    Also handles redacting sensitive context/extra fields automatically.
    """

    def __init__(self, redactor: Redactor = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redactor = redactor or Redactor()

    def format(self, record: logging.LogRecord) -> str:
        """Construct the core JSON payload for the log record."""
        payload: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "service": getattr(record, "service", "unknown"),
            "environment": getattr(record, "environment", "unknown"),
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Context injected by ContextInjectionFilter
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        if hasattr(record, "correlation_id"):
            payload["correlation_id"] = record.correlation_id

        # Exception info
        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }
        else:
            payload["exception"] = None

        # Any extra kwargs explicitly passed to logger.info("...", extra={"foo": "bar"})
        standard_keys = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "asctime",
            "service",
            "environment",
            "request_id",
            "correlation_id",
        }

        extra_data = {
            k: v
            for k, v in record.__dict__.items()
            if k not in standard_keys and not k.startswith("_")
        }

        # Merge extra fields into the root of the payload
        payload.update(extra_data)

        # Redact entire payload
        redacted_payload = self.redactor.redact(payload)

        return self.serialize(redacted_payload)

    def serialize(self, record_dict: Dict[str, Any]) -> str:
        """
        Abstract serialization point.
        Uses standard json but can be overridden with orjson if performance dictates.
        """
        return json.dumps(record_dict, default=str)
