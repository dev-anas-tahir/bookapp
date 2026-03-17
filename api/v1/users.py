from typing import Optional

from litestar import Controller, get, post
from litestar.params import Parameter

from dtos.user_dto import CreateUserDTO
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": lambda: UserService()}

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        create_dto = CreateUserDTO(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            date_of_birth=data.date_of_birth,
        )
        result = await user_service.create_user(create_dto)
        return UserResponse(
            id=result.id,
            first_name=result.first_name,
            last_name=result.last_name,
            email=result.email,
            date_of_birth=result.date_of_birth,
            created_at=result.created_at,
        )
