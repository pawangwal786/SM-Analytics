import contextvars
from typing import Optional

request_id_ctx_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id", default=None
)

correlation_id_ctx_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "correlation_id", default=None
)


def get_request_id() -> Optional[str]:
    return request_id_ctx_var.get()


def get_correlation_id() -> Optional[str]:
    return correlation_id_ctx_var.get()
