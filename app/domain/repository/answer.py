from typing import List

from domain.datasource.answer import AnswerModel
from domain.datasource.question import QuestionModel
from domain.datasource.user import UserModel
from domain.repository.base import BaseRepository
from sqlalchemy import select, update


class AnswerRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> QuestionModel | None:
        query = select(QuestionModel).where(QuestionModel.external_id == external_id)
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
        scalarResult = await self._session.scalars(query)
        result = scalarResult.all()

        return result  # type: ignore

    async def add(self, answer: AnswerModel) -> None:
        self._session.add(answer)

    async def edit(self, answer_external_id: str, user_id: int, answer: str) -> None:
        query = update(AnswerModel).where(AnswerModel.external_id == answer_external_id, UserModel.id == user_id).values({
            AnswerModel.answer: answer,
        })
        await self._session.execute(query)
