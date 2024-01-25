import pytest
from core.config import Config
from core.util.jwt import JWTUtil
from domain.datasource.user import UserModel
from domain.service.jwt import JWTSchema, JWTService
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
async def jwt_service(config: Config) -> JWTService:
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return JWTService(jwt_util=jwt_util)


@pytest.fixture(scope="function")
async def user_model(session: AsyncSession) -> UserModel:
    user_model = UserModel()
    session.add(instance=user_model)
    await session.commit()
    return user_model


@pytest.fixture(scope="function")
async def jwt_schema(jwt_service: JWTService, user_model: UserModel) -> JWTSchema:
    return jwt_service.create(external_id=str(user_model.external_id))
