from datetime import datetime, UTC

from schemas.user import UserCreate, UserUpdate, UserRead
from models.users import User


class UserService:
    """Service layer for user-related operations."""

    async def create_user(self, dto: UserCreate) -> UserRead:
        """Create a new user."""
        user = User(
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            date_of_birth=dto.date_of_birth,
        )
        await user.save()
        return UserRead(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=str(user.date_of_birth),
            created_at=str(user.created_at),
        )

    async def get_user(self, user_id: str) -> UserRead | None:
        """Retrieve a user by ID."""
        user = await User.objects().where(User.id == user_id).first()
        if not user:
            return None
        return UserRead(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=str(user.date_of_birth),
            created_at=str(user.created_at),
        )

    async def update_user(self, user_id: str, dto: UserUpdate) -> UserRead | None:
        """Update an existing user."""
        user = await User.objects().where(User.id == user_id).first()
        if not user:
            return None
        if dto.email is not None:
            user.email = dto.email
        if dto.first_name is not None:
            user.first_name = dto.first_name
        if dto.last_name is not None:
            user.last_name = dto.last_name
        if dto.date_of_birth is not None:
            user.date_of_birth = dto.date_of_birth
        await user.update()
        return UserRead(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=str(user.date_of_birth),
            created_at=str(user.created_at),
        )

    async def delete_user(self, user_id: str) -> None:
        """Soft-delete a user by ID."""
        user = await User.objects().where(User.id == user_id).first()
        if user:
            user.deleted_at = datetime.now(UTC)
            await user.update()
