import asyncio
import json
import logging

import pytest

from libs.observability.filters.redaction import Redactor
from libs.observability.formatters.json import JSONFormatter
from libs.observability.context.vars import (
    request_id_ctx_var,
    get_request_id,
    get_correlation_id,
)
from libs.observability.middleware.asgi import ObservabilityMiddleware


def test_redactor_exact_match():
    redactor = Redactor()
    data = {"Authorization": "Bearer secret", "normal_field": "safe"}
    result = redactor.redact(data)
    assert result["Authorization"] == "*****"
    assert result["normal_field"] == "safe"


def test_redactor_pattern_match():
    redactor = Redactor()
    data = {"db_password": "supersecret", "my_secret": "hidden"}
    result = redactor.redact(data)
    assert result["db_password"] == "*****"
    assert result["my_secret"] == "*****"


def test_json_formatter():
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    # Simulate ContextInjectionFilter
    record.request_id = "req-123"
    record.correlation_id = "corr-123"
    record.service = "test-service"
    record.environment = "testing"

    # Simulate extra field
    record.db_password = "mysecretpassword"
    record.duration_ms = 42.5

    formatter = JSONFormatter()
    formatted_str = formatter.format(record)

    parsed = json.loads(formatted_str)
    assert parsed["message"] == "Test message"
    assert parsed["request_id"] == "req-123"
    assert parsed["service"] == "test-service"
    assert parsed["level"] == "INFO"
    assert parsed["duration_ms"] == 42.5

    # Check that extra kwargs were hoisted and redacted
    assert parsed["db_password"] == "*****"
    # Verify we didn't inject "extra" as a sub-object
    assert "extra" not in parsed
    assert parsed["exception"] is None


@pytest.mark.asyncio
async def test_contextvar_isolation():
    # Helper to simulate an async request
    async def simulate_request(req_id: str):
        token = request_id_ctx_var.set(req_id)
        try:
            # Yield control back to event loop to prove isolation
            await asyncio.sleep(0.01)
            assert get_request_id() == req_id
        finally:
            request_id_ctx_var.reset(token)

    # Run two simulated requests concurrently with different IDs
    await asyncio.gather(simulate_request("req-A"), simulate_request("req-B"))


@pytest.mark.asyncio
async def test_asgi_middleware_id_generation():
    captured_req_id = None
    captured_corr_id = None

    async def mock_app(scope, receive, send):
        nonlocal captured_req_id, captured_corr_id
        captured_req_id = get_request_id()
        captured_corr_id = get_correlation_id()
        await send({"type": "http.response.start", "status": 200})
        await send({"type": "http.response.body"})

    middleware = ObservabilityMiddleware(mock_app)

    scope = {"type": "http", "method": "GET", "path": "/", "headers": []}

    async def receive():
        return {"type": "http.request"}

    messages_sent = []

    async def send(message):
        messages_sent.append(message)

    await middleware(scope, receive, send)

    assert captured_req_id is not None
    assert captured_corr_id is not None
    assert len(messages_sent) == 2
    assert messages_sent[0]["status"] == 200
    assert get_request_id() is None


@pytest.mark.asyncio
async def test_asgi_middleware_streaming_and_disconnect():
    async def mock_app(scope, receive, send):
        # Simulate a streaming response
        await send({"type": "http.response.start", "status": 206})
        await send({"type": "http.response.body", "body": b"chunk1", "more_body": True})

        # Simulate client disconnect mid-stream
        event = await receive()
        if event["type"] == "http.disconnect":
            return

        await send(
            {"type": "http.response.body", "body": b"chunk2", "more_body": False}
        )

    middleware = ObservabilityMiddleware(mock_app)

    scope = {"type": "http", "method": "GET", "path": "/stream", "headers": []}

    receive_events = [{"type": "http.request"}, {"type": "http.disconnect"}]

    async def receive():
        return receive_events.pop(0) if receive_events else {"type": "http.disconnect"}

    messages_sent = []

    async def send(message):
        messages_sent.append(message)

    await middleware(scope, receive, send)

    # Assert stream start was captured and context reset despite early exit
    assert messages_sent[0]["status"] == 206
    assert get_request_id() is None


@pytest.mark.asyncio
async def test_asgi_middleware_exception_handling():
    async def mock_app(scope, receive, send):
        await send({"type": "http.response.start", "status": 200})
        raise ValueError("Simulated catastrophic failure")

    middleware = ObservabilityMiddleware(mock_app)

    scope = {"type": "http", "method": "POST", "path": "/crash", "headers": []}

    async def receive():
        return {"type": "http.request"}

    async def send(message):
        pass

    with pytest.raises(ValueError, match="Simulated catastrophic failure"):
        await middleware(scope, receive, send)

    # Context should STILL be reset when an exception bubbles out
    assert get_request_id() is None
