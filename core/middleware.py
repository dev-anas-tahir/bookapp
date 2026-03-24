from uuid import uuid4

import structlog
from litestar.middleware.base import AbstractMiddleware
from litestar.types import Receive, Scope, Send


class RequestIdMiddleware(AbstractMiddleware):
    """Generate request_id and bind to structlog context for request tracing."""

    scopes = {"http", "websocket"}  # Apply to HTTP and WebSocket scopes

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        # Generate or extract request_id from header
        headers = dict(scope.get("headers", []))
        request_id_header = headers.get(b"x-request-id", b"").decode()
        request_id = request_id_header or str(uuid4())

        # Store in scope for access in route handlers
        scope["request_id"] = request_id

        # Bind to structlog context for all logs in this request
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        try:
            await self.app(scope, receive, send)
        finally:
            structlog.contextvars.clear_contextvars()


MIDDLEWARES = [RequestIdMiddleware]
