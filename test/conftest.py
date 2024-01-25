import asyncio
import logging
import os

import pytest
from api.server import fast_api
from core.config import Config, Env, EnvironmentKey, get_config
from core.db.model import BaseModel
from core.db.session import DatabaseSessionManager, db_manager, get_session
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    yield logger


@pytest.fixture(scope="function")
async def client(session: AsyncSession):
    async with AsyncClient(app=fast_api, base_url="http://test") as ac:

        async def _get_session():
            yield session

        fast_api.dependency_overrides[get_session] = _get_session
        yield ac


@pytest.fixture(scope="session")
async def config():
    return get_config()


@pytest.fixture(scope="session")
async def database_session_manager(config: Config) -> DatabaseSessionManager:
    db_manager.init(db_url=str(config.SQLALCHEMY_DATABASE_URI))
    yield db_manager
    await db_manager.close()


@pytest.fixture(scope="function")
async def session(database_session_manager: DatabaseSessionManager):
    async with database_session_manager.session() as session:
        yield session

    async with database_session_manager.session() as session:
        for table in reversed(BaseModel.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
