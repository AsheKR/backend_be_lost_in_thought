from domain.repository.user import UserModel, UserRepository
from domain.service.base import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()

    async def create_user(self) -> None:
        await self._user_repository.add(user=UserModel())
