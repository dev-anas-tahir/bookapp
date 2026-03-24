from litestar import Controller, post
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from apps.auth.dependencies import AUTH_DEPENDENCIES
from apps.auth.schema import LoginRequest, LoginResponse, SignupRequest, SignupResponse
from apps.auth.service import AuthService
from core.settings import settings


class AuthController(Controller):
    """Authentication controller handling signup/login."""

    path = "/auth"
    dependencies = AUTH_DEPENDENCIES

    @post(path="/signup")
    async def signup(
        self,
        auth_service: AuthService,
        request_id: str,
        data: SignupRequest,
    ) -> SignupResponse:
        """Register a new user.

        Args:
            auth_service: The authentication service
            request_id: Unique request identifier for logging
            data: User signup data

        Returns:
            Created user information without sensitive data
        """
        result = await auth_service.signup(data, request_id=request_id)
        return result

    @post(path="/login", status_code=HTTP_200_OK)
    async def login(
        self,
        auth_service: AuthService,
        request_id: str,
        data: LoginRequest,
    ) -> Response[LoginResponse]:
        result, refresh_token = await auth_service.login(data, request_id=request_id)
        # Set refresh token in cookie
        response = Response(content=result, status_code=HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.app_env != "dev",
            samesite="lax",
            path="/",
        )
        return response
