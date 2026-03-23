from litestar import Controller, post

from apps.auth.dependencies import AUTH_DEPENDENCIES
from apps.auth.schema import SignupRequest, SignupResponse
from apps.auth.service import AuthService


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
