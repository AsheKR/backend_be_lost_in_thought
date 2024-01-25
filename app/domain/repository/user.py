from core.db.model import BaseModel
from domain.repository.base import BaseRepository
from domain.string import TableName
from sqlalchemy import select


class UserModel(BaseModel):
    __tablename__ = TableName.user


class UserRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.external_id == external_id)
        return await self._session.scalar(query)

    async def add(self, user: UserModel) -> None:
        self._session.add(user)
