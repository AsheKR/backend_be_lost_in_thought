from domain.datasource.user import UserModel
from domain.repository.user import UserRepository
from domain.service.base import BaseService
from pydantic import UUID4, BaseModel


class InternalUserSchema(BaseModel):
    id: int
    external_id: UUID4


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def find_first_by_external_id(self, external_id: str) -> InternalUserSchema | None:
        user_model = await self._user_repository.find_first_by_external_id(external_id=external_id)
        if not user_model:
            return None

        return InternalUserSchema(
            id=user_model.id,
            external_id=user_model.external_id,
        )

    async def register(self) -> str:
        user_model = await self._user_repository.register()
        return user_model.external_id
