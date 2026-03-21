import msgspec


class UserRead(msgspec.Struct):
    """Schema for user responses."""
    
    id: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: str
    created_at: str


class UserCreate(msgspec.Struct):
    """Schema for creating new users."""
    
    email: str
    first_name: str
    last_name: str
    date_of_birth: str


class UserUpdate(msgspec.Struct):
    """Schema for updating existing users."""
    
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: str | None = None
