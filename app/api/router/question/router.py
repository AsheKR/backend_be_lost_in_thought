from api.router.question.response import QuestionResponse
from api.router.question.string import QuestionEndPoint
from api.util import get_current_user
from core.db.session import get_session
from domain.repository.question import QuestionRepository
from domain.service.question import QuestionService
from domain.service.user import UserSchema
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

question_router = APIRouter()


@question_router.get(path=QuestionEndPoint.recommendation)
async def recommendation_list(
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[QuestionResponse]:
    question_repository = QuestionRepository(
        session=session,
    )
    question_service = QuestionService(
        question_repository=question_repository,
    )
    question_list = await question_service.recommendation_list(
        user_id=user.id,
    )
    await session.commit()
    return [
        QuestionResponse(
            external_id=question.external_id,
            question=question.question,
        )
        for question in question_list
    ]
