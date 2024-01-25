from core.config import Config
from core.config import get_config as _get_config
from core.db.session import get_session
from core.util.jwt import JWTUtil
from domain.repository.answer import AnswerRepository
from domain.repository.question import QuestionRepository
from domain.repository.user import UserRepository
from domain.service.answer import AnswerService
from domain.service.jwt import JWTService
from domain.service.question import QuestionService
from domain.service.user import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_config() -> Config:
    return _get_config()


async def get_jwt_util(config: Config = Depends(get_config)) -> JWTUtil:
    return JWTUtil(
        secret_key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )


async def get_jwt_service(jwt_util: JWTUtil = Depends(get_jwt_util)) -> JWTService:
    return JWTService(
        jwt_util=jwt_util,
    )


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


async def get_question_repository(session: AsyncSession = Depends(get_session)) -> QuestionRepository:
    return QuestionRepository(session=session)


async def get_question_service(
    question_repository: QuestionRepository = Depends(get_question_repository),
) -> QuestionService:
    return QuestionService(question_repository=question_repository)


async def get_answer_repository(session: AsyncSession = Depends(get_session)) -> AnswerRepository:
    return AnswerRepository(session=session)


async def get_answer_service(answer_repository: AnswerRepository = Depends(get_answer_repository)) -> AnswerService:
    return AnswerService(answer_repository=answer_repository)
