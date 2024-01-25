from domain.repository.user import UserModel, UserRepository
from domain.service.base import BaseService
from pydantic import UUID4, BaseModel


class UserSchema(BaseModel):
    external_id: UUID4


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()

    async def find_first_by_external_id(self, external_id: str) -> UserSchema | None:
        user_model = await self._user_repository.find_first_by_external_id(external_id=external_id)
        if not user_model:
            return

        return UserSchema(
            external_id=user_model.external_id,
        )

    async def create_user(self) -> None:
        await self._user_repository.add(user=UserModel())
