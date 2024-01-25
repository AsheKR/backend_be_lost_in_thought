from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.router.delete.string import DeleteEndPoint
from api.router.depdendency import get_answer_service
from api.util import get_current_user
from core.db.session import get_session
from domain.service.answer import AnswerService
from domain.service.user import InternalUserSchema

delete_all_router = APIRouter()


@delete_all_router.post(path=DeleteEndPoint.delete_all)
async def delete_all(session: AsyncSession = Depends(get_session), user: InternalUserSchema = Depends(get_current_user), answer_service: AnswerService = Depends(get_answer_service), ) -> None:
    await answer_service.delete_all(user_id=user.id)
    await session.commit()
