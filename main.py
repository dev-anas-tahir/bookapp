import msgspec
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.response import Response

from api.health import health_check
from api.v1.router import v1_router
from core.exceptions import (
    DomainException,
    InfrastructureException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from core.middleware import MIDDLEWARES
from core.plugins import configure_structlog
from core.settings import settings

# Configure structlog on startup
configure_structlog()


def msgspec_encoder(value):
    """Custom type encoder for msgspec.Struct types."""
    if isinstance(value, msgspec.Struct):
        return msgspec.json.encode(value).decode()
    raise TypeError(f"Cannot encode type: {type(value)}")


def exception_handler_factory(exc_class: type[DomainException]):
    """Create exception handler for domain exceptions."""

    def handler(request, exc: exc_class) -> Response:
        return Response(
            content={"error": exc.message, "code": exc.error_code},
            status_code=exc.status_code,
        )

    return handler


# Exception handlers mapping
EXCEPTION_HANDLERS = {
    DomainException: exception_handler_factory(DomainException),
    UserAlreadyExistsException: exception_handler_factory(UserAlreadyExistsException),
    InvalidCredentialsException: exception_handler_factory(InvalidCredentialsException),
    InfrastructureException: exception_handler_factory(InfrastructureException),
}


# CORS configuration
cors_config = CORSConfig(
    allow_origins=["*"],  # Configure appropriately for production
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


# OpenAPI configuration
openapi_config = OpenAPIConfig(
    title="BookApp API",
    version="1.0.0",
    description="Book management API with authentication",
)


# Type encoders for custom serialization
type_encoders = {msgspec.Struct: msgspec_encoder}


app = Litestar(
    route_handlers=[v1_router, health_check],
    middleware=MIDDLEWARES,
    exception_handlers=EXCEPTION_HANDLERS,
    debug=settings.app_debug,
    cors_config=cors_config,
    openapi_config=openapi_config,
    type_encoders=type_encoders,
)
