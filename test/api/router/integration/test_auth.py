from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4

from assertpy import assert_that
from core.config import Config
from core.util.jwt import JWTUtil
from domain.datasource.user import UserModel
from domain.service.jwt import JWTSchema, JWTService
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_login(client: AsyncClient, user_model: UserModel):
    response = await client.post(
        url="/auth/login",
        json={
            "id": str(user_model.external_id),
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data["access_token"]).is_not_none()
    assert_that(response_data["refresh_token"]).is_not_none()


async def test_login_fail_when_external_id_does_not_exist(client: AsyncClient):
    response = await client.post(
        url="/auth/login",
        json={
            "id": str(uuid4()),
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data["error_code"]).is_equal_to("AUTH__FAIL")


async def test_refresh(config: Config, client: AsyncClient, user_model: UserModel, jwt_service: JWTService):
    with freeze_time(datetime.utcnow() - config.JWT_ACCESS_TOKEN_EXPIRE_DELTA - timedelta(hours=1)):
        jwt_schema = jwt_service.create(external_id=str(user_model.external_id))

    response = await client.post(
        url="/auth/refresh",
        json={
            "refresh_token": jwt_schema.refresh_token,
        },
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data["access_token"]).is_not_none()
    assert_that(response_data["refresh_token"]).is_not_none()


async def test_refresh_fail_when_token_decode_exception(client: AsyncClient):
    response = await client.post(
        url="/auth/refresh",
        json={
            "refresh_token": "refresh_token",
        },
        headers={
            "Authorization": "JWT access_token",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data["error_code"]).is_equal_to("AUTH__DECODE_TOKEN")


async def test_refresh_fail_when_access_token_expired_exception(
    config: Config,
    client: AsyncClient,
    user_model: UserModel,
    jwt_service: JWTService,
):
    with freeze_time(datetime.utcnow() - config.JWT_REFRESH_TOKEN_EXPIRE_DELTA - timedelta(hours=1)):
        jwt_schema = jwt_service.create(external_id=str(user_model.external_id))

    response = await client.post(
        url="/auth/refresh",
        json={
            "refresh_token": jwt_schema.refresh_token,
        },
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    response_data = response.json()
    assert_that(response_data["error_code"]).is_equal_to("AUTH__EXPIRED_TOKEN")
