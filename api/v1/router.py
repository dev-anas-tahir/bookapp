from litestar import Router

from apps.auth.router import AuthController

v1_router = Router(
    path="/v1",
    route_handlers=[AuthController],
)
