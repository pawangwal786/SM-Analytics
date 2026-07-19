import logging
import os
import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Ensure backend directory is in the path to allow imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.libs.observability.context.vars import get_request_id
from backend.libs.observability.logging.setup import configure_logging
from backend.libs.observability.middleware.asgi import ObservabilityMiddleware
from backend.services.auth.app.core.config import get_settings

settings = get_settings()

# 1. Configure Observability globally before creating the app
configure_logging(
    service_name=settings.app_name,
    environment=settings.environment.value,
    log_level=settings.log_level,
)

app = FastAPI(title="SM Analytics Auth Service", version=settings.version)

# 2. Add Observability ASGI Middleware
app.add_middleware(ObservabilityMiddleware)

logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catch unhandled exceptions, log them with full context,
    and return a sanitized 500 response.
    """
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "request_id": get_request_id()},
    )


@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called", extra={"status": "healthy"})
    return {"status": "ok", "service": settings.app_name}
