import secrets

import structlog
from argon2 import PasswordHasher

from apps.auth.models import (
    Permission,
    Role,
    RolePermission,
    User,
    UserPermission,
    UserRole,
)
from apps.auth.schema import LoginRequest, LoginResponse, SignupRequest, SignupResponse
from core.exceptions import (
    InfrastructureException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from core.security import create_access_token

ph = PasswordHasher()
logger = structlog.get_logger()


class AuthService:
    async def signup(self, data: SignupRequest, request_id: str) -> SignupResponse:
        """
        Sign up a new user with proper validation, transaction safety, and logging.

        Args:
            data: SignupRequest containing user registration data
            request_id: Unique request identifier for tracking

        Returns:
            UserResponse: Minimal user data excluding sensitive information

        Raises:
            UserAlreadyExistsException: If user with email already exists
            InfrastructureException: If viewer role does not exist in the database
        """

        # Check if user already exists
        existing_user = await User.select().where(User.email == data.email).first()
        if existing_user:
            raise UserAlreadyExistsException(data.email)

        # Get the viewer role to ensure it exists
        viewer_role = await Role.select().where(Role.name == "viewer").first()
        if not viewer_role:
            raise InfrastructureException(
                "Viewer role does not exist in the database, please seed the database"
            )

        # Get the db
        db = User._meta.db

        # Use transaction to ensure atomicity of user creation and role assignment
        async with db.transaction():
            # Hash the password using argon2
            hashed_password = ph.hash(data.password)

            # Create the user in the database
            user = User(
                email=data.email,
                first_name=data.first_name,
                last_name=data.last_name,
                password=hashed_password,
                date_of_birth=data.date_of_birth,
            )
            await user.save()

            # Assign the viewer role to the user
            user_role = UserRole(user=user.id, role=viewer_role["id"])
            await user_role.save()

        # Log the successful user creation
        logger.info(
            "user.signup",
            user_id=str(user.id),
            email=data.email,
            request_id=request_id,
        )

        # Return minimal user data using response schema (excluding password)
        return SignupResponse.from_model(user)

    async def login(self, data: LoginRequest, request_id: str) -> LoginResponse:
        """
        Login a user with proper validation, transaction safety, and logging.

        Args:
            data: LoginRequest containing user login data
            request_id: Unique request identifier for tracking

        Returns:
            LoginResponse: Access token for the user

        Raises:
            InvalidCredentialsException: If user credentials are invalid
        """
        user_row = (
            await User.select(User.id, User.email, User.password)
            .where(User.email == data.email)
            .first()
        )
        if not user_row:
            raise InvalidCredentialsException()

        user_id = user_row["id"]
        email = user_row["email"]

        try:
            ph.verify(user_row["password"], data.password)
        except Exception as e:
            raise InvalidCredentialsException() from e

        user_role_rows = await UserRole.select(UserRole.role).where(
            UserRole.user == user_id
        )
        role_ids = [row["role"] for row in user_role_rows]

        role_rows = (
            await Role.select(Role.name).where(Role.id.is_in(role_ids))
            if role_ids
            else []
        )
        roles = [row["name"] for row in role_rows]

        role_permission_rows = (
            await RolePermission.select(RolePermission.permission).where(
                RolePermission.role.is_in(role_ids)
            )
            if role_ids
            else []
        )
        role_permission_ids = [row["permission"] for row in role_permission_rows]

        user_permission_rows = await UserPermission.select(
            UserPermission.permission
        ).where(UserPermission.user == user_id)
        user_permission_ids = [row["permission"] for row in user_permission_rows]

        permission_ids = list({*role_permission_ids, *user_permission_ids})
        permission_rows = (
            await Permission.select(Permission.name).where(
                Permission.id.is_in(permission_ids)
            )
            if permission_ids
            else []
        )
        permissions = [row["name"] for row in permission_rows]

        access_token = create_access_token(
            user_id=str(user_id),
            username=email,
            roles=roles,
            permissions=permissions,
        )

        refresh_token = secrets.token_urlsafe(64)

        logger.info(
            "user.login",
            user_id=str(user_id),
            email=email,
            request_id=request_id,
        )

        return LoginResponse(access_token=access_token), refresh_token
