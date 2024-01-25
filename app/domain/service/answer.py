from typing import List

from domain.datasource.answer import AnswerModel
from domain.repository.answer import AnswerRepository
from domain.service.base import BaseService
from pydantic import UUID4, BaseModel


class AnswerSchema(BaseModel):
    external_id: UUID4
    answer: str


class InternalAnswerSchema(BaseModel):
    id: int


class AnswerService(BaseService):
    def __init__(self, answer_repository: AnswerRepository):
        self._answer_repository = answer_repository

    async def find_first_by_external_id(self, external_id: str) -> InternalAnswerSchema | None:
        answer_model = await self._answer_repository.find_first_by_external_id(external_id=external_id)
        if not answer_model:
            return None

        return InternalAnswerSchema(
            id=answer_model.id,
        )

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

    async def edit(self, answer_external_id: str, user_id: int, answer: str) -> None:
        await self._answer_repository.edit(
            answer_external_id=answer_external_id,
            user_id=user_id,
            answer=answer,
        )
