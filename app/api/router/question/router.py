from api.router.depdendency import get_question_service
from api.router.question.response import AnsweredQuestionResponse, QuestionResponse
from api.router.question.string import QuestionEndPoint
from api.util import get_current_user
from core.db.session import get_session
from domain.repository.question import QuestionRepository
from domain.service.question import QuestionService
from domain.service.user import InternalUserSchema
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

question_router = APIRouter()


@question_router.get(path=QuestionEndPoint.list)
async def answered_question_list(
    limit: int = 20,
    offset: int = 0,
    user: InternalUserSchema = Depends(get_current_user),
    question_service: QuestionService = Depends(get_question_service),
) -> list[AnsweredQuestionResponse]:
    _answered_question_list = await question_service.answered_list(
        user_id=user.id,
        limit=limit,
        offset=offset,
    )
    return [
        AnsweredQuestionResponse(
            id=answered_question.id,
            question=answered_question.question,
        )
        for answered_question in _answered_question_list
    ]


@question_router.get(path=QuestionEndPoint.recommendation)
async def recommendation_list(
    user: InternalUserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    question_service: QuestionService = Depends(get_question_service),
) -> list[QuestionResponse]:
    question_list = await question_service.recommendation_list(
        user_id=user.id,
    )
    await session.commit()
    return [
        QuestionResponse(
            id=question.external_id,
            question=question.question,
        )
        for question in question_list
    ]
