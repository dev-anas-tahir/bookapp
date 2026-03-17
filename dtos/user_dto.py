import msgspec


class UserDTO(msgspec.Struct):
    """Data Transfer Object for User entity."""

    id: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: str
    created_at: str


class CreateUserDTO(msgspec.Struct):
    """DTO for creating new users."""

    email: str
    first_name: str
    last_name: str
    date_of_birth: str


class UpdateUserDTO(msgspec.Struct):
    """DTO for updating existing users."""

    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: str | None = None
