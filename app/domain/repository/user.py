from core.db.model import BaseModel
from domain.datasource.user import UserModel
from domain.repository.base import BaseRepository
from sqlalchemy import select


class UserRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.delete_datetime == None, UserModel.external_id == external_id)
        return await self._session.scalar(query)  # type: ignore

    async def register(self) -> UserModel:
        user_model = UserModel()
        self._session.add(user_model)
        await self._session.flush()
        return user_model
