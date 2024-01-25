from typing import List

from domain.datasource.answer import AnswerModel
from domain.repository.answer import AnswerRepository
from domain.service.base import BaseService
from pydantic import UUID4, BaseModel


class AnswerSchema(BaseModel):
    external_id: UUID4
    answer: str


class AnswerService(BaseService):
    def __init__(self, answer_repository: AnswerRepository):
        self._answer_repository = answer_repository

    async def list(self, question_external_id: str, user_id: int, limit: int, offset: int) -> List[AnswerSchema]:
        answer_list = await self._answer_repository.list(
            question_external_id=question_external_id, user_id=user_id, limit=limit, offset=offset
        )

        return [
            AnswerSchema(
                external_id=answer.external_id,
                answer=answer.answer,
            )
            for answer in answer_list
        ]

    async def add(self, question_id: int, user_id: int, answer: str) -> None:
        await self._answer_repository.add(
            answer=AnswerModel(
                answer=answer,
                question_id=question_id,
                user_id=user_id,
            ),
        )
