from typing import List

from api.exception import UnprocessableEntity
from api.router.answer.request import AddAnswerRequest, EditAnswerRequest
from api.router.answer.response import AnswerResponse
from api.router.answer.string import AnswerDetailEndPoint, AnswerEndPoint
from api.router.depdendency import get_answer_service, get_question_service
from api.util import get_current_user
from core.db.session import get_session
from domain.repository.answer import AnswerRepository
from domain.repository.question import QuestionRepository
from domain.service.answer import AnswerService
from domain.service.exception import DoesNotExist
from domain.service.question import QuestionService
from domain.service.user import UserSchema
from fastapi import APIRouter, Depends
from pydantic import UUID4
from result import Err
from sqlalchemy.ext.asyncio import AsyncSession

answer_detail_router = APIRouter()
answer_router = APIRouter()


@answer_router.get(path=AnswerEndPoint.list)
async def list(
    question_id: UUID4,
    limit: int = 20,
    offset: int = 0,
    user: UserSchema = Depends(get_current_user),
    answer_service: AnswerService = Depends(get_answer_service),
) -> List[AnswerResponse]:
    answer_list = await answer_service.list(
        question_external_id=str(question_id),
        user_id=user.id,
        limit=limit,
        offset=offset,
    )
    return [
        AnswerResponse(
            id=answer.external_id,
            answer=answer.answer,
        )
        for answer in answer_list
    ]


@answer_router.post(path=AnswerEndPoint.add)
async def add(
    question_id: UUID4,
    request: AddAnswerRequest,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    answer_service: AnswerService = Depends(get_answer_service),
    question_service: QuestionService = Depends(get_question_service),
) -> None:
    question_schema = await question_service.find_first_by_external_id(external_id=str(question_id))
    if not question_schema:
        raise UnprocessableEntity

    await answer_service.add(
        user_id=user.id,
        question_id=question_schema.id,
        answer=request.answer,
    )

    await session.commit()


@answer_detail_router.patch(path=AnswerDetailEndPoint.edit)
async def edit(
    answer_id: UUID4,
    request: EditAnswerRequest,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    answer_service: AnswerService = Depends(get_answer_service),
) -> None:
    result = await answer_service.edit(
        answer_external_id=str(answer_id),
        user_id=user.id,
        answer=request.answer,
    )

    match result:
        case Err(exception):
            match exception:
                case DoesNotExist():
                    raise UnprocessableEntity

    await session.commit()


@answer_detail_router.delete(path=AnswerDetailEndPoint.delete)
async def delete(
    answer_id: UUID4,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    answer_service: AnswerService = Depends(get_answer_service),
) -> None:
    result = await answer_service.delete(
        answer_external_id=str(answer_id),
        user_id=user.id,
    )

    match result:
        case Err(exception):
            match exception:
                case DoesNotExist():
                    raise UnprocessableEntity

    await session.commit()
