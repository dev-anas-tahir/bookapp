import re
from datetime import date
from typing import Annotated

import msgspec

# Reusable constrained types - msgspec best practice
EmailStr = Annotated[
    str,
    msgspec.Meta(
        min_length=5,
        max_length=254,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        title="Email",
        description="Email address.",
        examples=["user@example.com"],
        extra_json_schema={"format": "email"},
    ),
]

# Password with minimum length constraint - pattern validation done in __post_init__
# since msgspec pattern can't validate complex password rules easily
PasswordStr = Annotated[
    str,
    msgspec.Meta(min_length=8, max_length=128),
]

# Name fields with reasonable length constraints
NameStr = Annotated[
    str,
    msgspec.Meta(min_length=1, max_length=100),
]


class SignupRequest(msgspec.Struct):
    """Schema for signup requests with msgspec Meta constraints."""

    email: EmailStr
    first_name: NameStr
    last_name: NameStr
    password: PasswordStr
    date_of_birth: date  # Accepts ISO format: YYYY-MM-DD

    def __post_init__(self):
        # Only cross-field validation remains here
        # msgspec handles type/constraints validation automatically at decode time
        self._validate_password_strength()

    def _validate_password_strength(self):
        """Validate password complexity requirements (cross-field check)."""
        if not re.search(r"[A-Z]", self.password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", self.password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", self.password):
            raise ValueError("Password must contain at least one number")


class SignupResponse(msgspec.Struct):
    """Schema for user response (excludes sensitive fields like password)."""

    id: str
    email: EmailStr  # Reuse constrained type
    first_name: str
    last_name: str
    date_of_birth: date  # msgspec serializes to ISO format (YYYY-MM-DD)

    @classmethod
    def from_model(cls, user_model) -> "SignupResponse":
        """Create SignupResponse from User model instance."""
        return cls(
            id=str(user_model.id),
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            date_of_birth=user_model.date_of_birth,  # Piccolo Date -> Python date
        )
