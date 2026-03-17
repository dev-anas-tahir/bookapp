import msgspec


class UserCreate(msgspec.Struct):
    """
    Schema for creating users
    """

    first_name: str
    last_name: str
    email: str
    date_of_birth: str


class UserUpdate(msgspec.Struct):
    """
    Schema for updating users
    """

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    date_of_birth: str | None = None


class UserResponse(msgspec.Struct):
    """
    Schema for user responses
    """

    id: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    created_at: str
