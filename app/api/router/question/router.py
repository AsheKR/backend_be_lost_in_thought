from datetime import datetime

from api.depdendency import get_question_service
from api.exception import UnprocessableEntity
from api.router.question.response import AnsweredQuestionResponse, QuestionResponse
from api.router.question.string import QuestionEndPoint
from api.util.auth import get_current_user
from api.util.language import AcceptLanguageHeader
from core.db.session import get_session
from core.language import SupportLanguage
from domain.service.question import QuestionService
from domain.service.user import InternalUserSchema
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

question_router = APIRouter()


@question_router.get(path=QuestionEndPoint.list)
async def answered_question_list(
    start_datetime: datetime,
    end_datetime: datetime,
    limit: int = Query(default=20, lt=21),
    offset: int = 0,
    user: InternalUserSchema = Depends(get_current_user),
    question_service: QuestionService = Depends(get_question_service),
    accept_language: SupportLanguage = Depends(AcceptLanguageHeader()),
) -> list[AnsweredQuestionResponse]:
    if (end_datetime - start_datetime).days > 31:
        raise UnprocessableEntity

    _answered_question_list = await question_service.answered_list(
        user_id=user.id,
        language_code=accept_language,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        limit=limit,
        offset=offset,
    )
    return [
        AnsweredQuestionResponse(
            id=answered_question.id,
            question=answered_question.question,
            answer_count=answered_question.answer_count,
            answer_datetime=answered_question.answer_datetime,
        )
        for answered_question in _answered_question_list
    ]


@question_router.get(path=QuestionEndPoint.recommendation)
async def recommendation_list(
    user: InternalUserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    question_service: QuestionService = Depends(get_question_service),
    accept_language: SupportLanguage = Depends(AcceptLanguageHeader()),
) -> list[QuestionResponse]:
    question_list = await question_service.recommendation_list(
        user_id=user.id,
        language_code=accept_language,
    )
    await session.commit()
    return [
        QuestionResponse(
            id=question.external_id,
            question=question.question,
        )
        for question in question_list
    ]
