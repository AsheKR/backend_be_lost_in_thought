from typing import List

from domain.datasource.answer import AnswerModel
from domain.datasource.question import QuestionModel
from domain.datasource.user import UserModel
from domain.repository.base import BaseRepository
from sqlalchemy import delete, select, update


class AnswerRepository(BaseRepository):
    async def find_first_by_external_id_and_user_id(self, external_id: str, user_id: int) -> AnswerModel | None:
        query = select(AnswerModel).where(AnswerModel.external_id == external_id, AnswerModel.user_id == user_id)
        return await self._session.scalar(query)  # type: ignore

    async def list(self, question_external_id: str, user_id: int, limit: int, offset: int) -> List[AnswerModel]:
        query = (
            select(AnswerModel)
            .join(QuestionModel)
            .join(UserModel)
            .where(
                QuestionModel.external_id == question_external_id,
                UserModel.id == user_id,
            )
            .limit(limit=limit)
            .offset(offset=offset)
            .order_by(AnswerModel.id)
        )
        scalar_result = await self._session.scalars(query)
        result = scalar_result.all()

        return result  # type: ignore

    async def add(self, answer_model: AnswerModel) -> None:
        self._session.add(answer_model)

    async def edit(self, answer_model: AnswerModel, answer: str) -> None:
        answer_model.answer = answer
        self._session.add(answer_model)

    async def delete(self, answer_model: AnswerModel) -> None:
        await self._session.delete(answer_model)
