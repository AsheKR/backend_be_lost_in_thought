from datetime import datetime
from typing import List

from domain.datasource.answer import AnswerModel
from domain.repository.answer import AnswerRepository
from domain.service.base import BaseService
from domain.service.exception import DoesNotExist
from pydantic import UUID4, BaseModel
from result import Err, Ok, Result


class AnswerSchema(BaseModel):
    external_id: UUID4
    answer: str
    create_datetime: datetime


class InternalAnswerSchema(BaseModel):
    id: int
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
                create_datetime=answer.create_datetime,
            )
            for answer in answer_list
        ]

    async def add(self, question_id: int, user_id: int, answer: str) -> None:
        await self._answer_repository.add(
            answer_model=AnswerModel(
                answer=answer,
                question_id=question_id,
                user_id=user_id,
            ),
        )

    async def edit(self, answer_external_id: str, user_id: int, answer: str) -> Result[None, DoesNotExist]:
        answer_model = await self._answer_repository.find_first_by_external_id_and_user_id(
            external_id=answer_external_id,
            user_id=user_id,
        )
        if not answer_model:
            return Err(DoesNotExist())

        await self._answer_repository.edit(
            answer_model=answer_model,
            answer=answer,
        )
        return Ok(None)

    async def delete(self, answer_external_id: str, user_id: int) -> Result[None, DoesNotExist]:
        answer_model = await self._answer_repository.find_first_by_external_id_and_user_id(
            external_id=answer_external_id,
            user_id=user_id,
        )
        if not answer_model:
            raise Err(DoesNotExist())

        await self._answer_repository.delete(answer_model=answer_model)
        return Ok(None)

    async def delete_all(self, user_id: int) -> None:
        await self._answer_repository.delete_all(
            user_id=user_id,
        )
