from litestar import Controller, get, post

from schemas.user import UserCreate, UserRead
from services.user_service import UserService


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": lambda: UserService()}

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserRead:
        result = await user_service.create_user(data)
        return result
