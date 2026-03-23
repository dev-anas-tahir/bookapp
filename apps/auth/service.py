import structlog
from argon2 import PasswordHasher

from apps.auth.models import Role, User, UserRole
from apps.auth.schema import SignupRequest, SignupResponse
from core.exceptions import InfrastructureException, UserAlreadyExistsException

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
        existing_user = await User.select().where(
            User.email == data.email
        ).first()
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

            print(viewer_role)

            # Assign the viewer role to the user
            user_role = UserRole(user=user.id, role=viewer_role["id"])
            await user_role.save()

        # Log the successful user creation
        logger.ainfo(
            "user.created",
            user_id=str(user.id),
            email=data.email,
            request_id=request_id,
        )

        # Return minimal user data using response schema (excluding password)
        return SignupResponse.from_model(user)
