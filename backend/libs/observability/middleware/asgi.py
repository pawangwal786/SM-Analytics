import logging
import time
import uuid
from contextvars import Token

from backend.libs.observability.context.vars import correlation_id_ctx_var, request_id_ctx_var

logger = logging.getLogger(__name__)


class ObservabilityMiddleware:
    """
    Pure ASGI middleware for observability.
    - Intercepts X-Request-ID and X-Correlation-ID.
    - Binds them to contextvars for the lifecycle of the request.
    - Resets contextvars afterwards.
    - Logs request start, completion, and latency.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            # Pass through WebSocket and lifespan scopes
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))

        # ASGI headers are bytes and lowercase
        req_id_header = headers.get(b"x-request-id")
        corr_id_header = headers.get(b"x-correlation-id")

        request_id = req_id_header.decode() if req_id_header else str(uuid.uuid4())
        correlation_id = corr_id_header.decode() if corr_id_header else str(uuid.uuid4())

        # Set context variables and store tokens for cleanup
        req_token: Token = request_id_ctx_var.set(request_id)
        corr_token: Token = correlation_id_ctx_var.set(correlation_id)

        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "/")

        start_time = time.perf_counter()

        status_code: int = 500

        # Wrapper to intercept the response status code
        async def wrapped_send(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 500)
            await send(message)

        try:
            # We don't log the start of every request by default unless debug is on,
            # to avoid log spam, but let's log the completion.
            await self.app(scope, receive, wrapped_send)
        except Exception:
            # The exception will bubble up, but we can log the failure here
            logger.exception(f"Unhandled exception processing request: {method} {path}")
            raise
        finally:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            # Log completion
            if status_code >= 500:
                level = logging.ERROR
            elif status_code >= 400:
                level = logging.WARNING
            else:
                level = logging.INFO

            logger.log(
                level,
                f"HTTP {method} {path} {status_code}",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration_ms": round(elapsed_ms, 2),
                },
            )

            # Reset contextvars to prevent leakage across async tasks
            request_id_ctx_var.reset(req_token)
            correlation_id_ctx_var.reset(corr_token)
