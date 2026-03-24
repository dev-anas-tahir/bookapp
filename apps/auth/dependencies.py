"""Dependency providers for auth domain."""

from typing import TYPE_CHECKING

from litestar.di import Provide

from apps.auth.service import AuthService

if TYPE_CHECKING:
    from litestar.types import Scope


async def provide_auth_service() -> AuthService:
    """Provide AuthService instance."""
    return AuthService()


def provide_request_id(scope: "Scope") -> str:
    """Extract request_id from ASGI scope (injected by RequestIdMiddleware)."""
    return scope.get("request_id", "unknown")


# Dependency map for auth controller
AUTH_DEPENDENCIES = {
    "auth_service": Provide(provide_auth_service),
    "request_id": Provide(provide_request_id, sync_to_thread=False),
}
