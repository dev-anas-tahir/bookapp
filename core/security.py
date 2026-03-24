from datetime import UTC, datetime, timedelta

import jwt

from core.settings import settings


def create_access_token(
    user_id: str,
    username: str,
    roles: list[str],
    permissions: list[str],
) -> str:
    to_encode = {
        "user_id": user_id,
        "username": username,
        "roles": roles,
        "permissions": permissions,
    }
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt
