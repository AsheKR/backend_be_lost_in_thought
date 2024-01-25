from typing import TYPE_CHECKING

from core.db.model import BaseModel
from domain.repository.base import BaseRepository
from domain.string import TableName
from sqlalchemy import select
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from domain.repository.question import SuggestedQuestionModel


class UserModel(BaseModel):
    __tablename__ = TableName.user

    suggested_question_list: Mapped["SuggestedQuestionModel"] = relationship(back_populates="user")


class UserRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.external_id == external_id)
        return await self._session.scalar(query)  # type: ignore

    async def add(self, user: UserModel) -> None:
        self._session.add(user)
