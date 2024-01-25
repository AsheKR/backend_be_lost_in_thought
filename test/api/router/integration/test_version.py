from http import HTTPStatus

from assertpy import assert_that
from httpx import AsyncClient

from core.config import Config


async def test_can_update_android(client: AsyncClient, config: Config):
    major, minor, patch = map(int, config.ANDROID_LATEST_VERSION.split('.'))
    response = await client.get(
        url=f"/can-update",
        headers={
            'x-os-name': 'Android',
            'x-app-version': f'{major}.{minor}.{patch - 1}',
        }
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    assert_that(response.json()).is_equal_to(True)


async def test_can_not_update_android(client: AsyncClient, config: Config):
    response = await client.get(
        url=f"/can-update",
        headers={
            'x-os-name': 'Android',
            'x-app-version': config.ANDROID_LATEST_VERSION,
        }
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    assert_that(response.json()).is_equal_to(False)


async def test_can_update_ios(client: AsyncClient, config: Config):
    major, minor, patch = map(int, config.IOS_LATEST_VERSION.split('.'))
    response = await client.get(
        url=f"/can-update",
        headers={
            'x-os-name': 'iOS',
            'x-app-version': f'{major}.{minor}.{patch - 1}',
        }
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    assert_that(response.json()).is_equal_to(True)


async def test_can_not_update_ios(client: AsyncClient, config: Config):
    response = await client.get(
        url=f"/can-update",
        headers={
            'x-os-name': 'iOS',
            'x-app-version': config.IOS_LATEST_VERSION,
        }
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    assert_that(response.json()).is_equal_to(False)
