from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4

from assertpy import assert_that
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from api.server import fast_api
from core.config import Config, get_config
from core.util.jwt import JWTUtil
from domain.repository.user import UserModel, UserRepository
from domain.service.jwt import JWTService


async def test_login(client: AsyncClient, session: async_scoped_session[AsyncSession]):
    user_model = UserModel()
    session.add(instance=user_model)
    await session.flush()

    response = await client.post(url='/auth/login', json={
        "external_id": str(user_model.external_id),
    })

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data['access_token']).is_not_none()
    assert_that(response_data['refresh_token']).is_not_none()


async def test_login_fail_when_external_id_does_not_exist(client: AsyncClient):
    response = await client.post(url='/auth/login', json={
        "external_id": str(uuid4()),
    })

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data['error_code']).is_equal_to('AUTH__FAIL')


async def test_refresh(config: Config, client: AsyncClient, session: async_scoped_session[AsyncSession]):
    user_model = UserModel()
    session.add(instance=user_model)
    await session.flush()

    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    with freeze_time(datetime.utcnow() - config.JWT_ACCESS_TOKEN_EXPIRE_DELTA - timedelta(hours=1)):
        jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.post(
        url='/auth/refresh', 
        json={
            "refresh_token": jwt_schema.refresh_token,
        },
        headers={
            'Authorization': f'JWT {jwt_schema.access_token}',
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data['access_token']).is_not_none()
    assert_that(response_data['refresh_token']).is_not_none()


async def test_refresh_fail_when_token_decode_exception(client: AsyncClient):
    response = await client.post(
        url='/auth/refresh', 
        json={
            "refresh_token": 'refresh_token',
        },
        headers={
            'Authorization': f'JWT access_token',
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data['error_code']).is_equal_to('AUTH__DECODE_TOKEN')


async def test_refresh_fail_when_access_token_expired_exception(config: Config, client: AsyncClient, session: async_scoped_session[AsyncSession]):
    user_model = UserModel()
    session.add(instance=user_model)
    await session.flush()

    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    with freeze_time(datetime.utcnow() - config.JWT_REFRESH_TOKEN_EXPIRE_DELTA - timedelta(hours=1)):
        jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.post(
        url='/auth/refresh', 
        json={
            "refresh_token": jwt_schema.refresh_token,
        },
        headers={
            'Authorization': f'JWT {jwt_schema.access_token}',
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data['error_code']).is_equal_to('AUTH__EXPIRED_TOKEN')
