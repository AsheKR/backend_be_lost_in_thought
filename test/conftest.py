import asyncio
import logging
import os
from httpx import AsyncClient

import pytest
from api.server import fast_api
from core.config import Env, EnvironmentKey, get_config
from core.db.session import get_session


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


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=fast_api, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope="session")
async def config():
    return get_config()


@pytest.fixture(scope="function")
async def session(logger: logging.Logger):
    session = get_session()
    connection = await session.connection()

    yield session

    await connection.rollback()
    await connection.close()
