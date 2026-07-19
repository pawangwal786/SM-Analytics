import contextvars

request_id_ctx_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)

correlation_id_ctx_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


def get_request_id() -> str | None:
    return request_id_ctx_var.get()


def get_correlation_id() -> str | None:
    return correlation_id_ctx_var.get()
