from core.db.model import BaseModel
from domain.repository.base import BaseRepository
from domain.string import TableName


class UserModel(BaseModel):
    __tablename__ = TableName.user


class UserRepository(BaseRepository):
    async def add(self, user: UserModel) -> None:
        self._session.add(user)
        await self._session.commit()
