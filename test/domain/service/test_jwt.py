from unittest.mock import patch

from assertpy import assert_that
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from domain.service.jwt import JWTService
from result import Err, Ok


async def test_create():
    with patch(
        target="core.util.jwt.JWTUtil.encode",
        side_effect=[
            "access_token",
            "refresh_token",
        ],
    ) as encode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        result_jwt_schema = jwt_service.create(external_id="external_id")

        assert_that(encode.call_count).is_same_as(2)
        assert_that(result_jwt_schema.access_token).is_same_as("access_token")
        assert_that(result_jwt_schema.refresh_token).is_same_as("refresh_token")


async def test_refresh():
    with patch(
        target="core.util.jwt.JWTUtil.decode",
        side_effect=[JWTExpiredException(), {}, {"sub": "external_id"}],
    ) as decode:
        with patch(
            target="core.util.jwt.JWTUtil.encode",
            side_effect=[
                "access_token",
                "refresh_token",
            ],
        ) as encode:
            jwt_util = JWTUtil(secret_key="", algorithm="")
            jwt_service = JWTService(
                jwt_util=jwt_util,
            )
            refresh_result = jwt_service.refresh(
                access_token="access_token",
                refresh_token="refresh_token",
            )

            assert_that(refresh_result).is_instance_of(Ok)
            assert_that(decode.call_count).is_same_as(3)

            assert_that(encode.call_count).is_same_as(2)
            assert_that(refresh_result.ok_value.access_token).is_same_as("access_token")
            assert_that(refresh_result.ok_value.refresh_token).is_same_as("refresh_token")


async def test_refresh_fail_when_access_token_decode_fail():
    with patch(target="core.util.jwt.JWTUtil.decode", side_effect=JWTDecodeException()) as decode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        refresh_result = jwt_service.refresh(
            access_token="access_token",
            refresh_token="refresh_token",
        )

        assert_that(decode.call_count).is_same_as(1)
        assert_that(refresh_result).is_instance_of(Err)
        assert_that(refresh_result.err_value).is_instance_of(JWTDecodeException)


async def test_refresh_fail_when_access_token_not_expired():
    with patch(target="core.util.jwt.JWTUtil.decode", return_value={}) as decode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        refresh_result = jwt_service.refresh(
            access_token="access_token",
            refresh_token="refresh_token",
        )

        assert_that(decode.call_count).is_same_as(1)
        assert_that(refresh_result).is_instance_of(Err)
        assert_that(refresh_result.err_value).is_instance_of(JWTDecodeException)


async def test_refresh_fail_when_refresh_token_decode_fail():
    with patch(
        target="core.util.jwt.JWTUtil.decode", side_effect=[JWTExpiredException(), JWTDecodeException()]
    ) as decode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        refresh_result = jwt_service.refresh(
            access_token="access_token",
            refresh_token="refresh_token",
        )

        assert_that(decode.call_count).is_same_as(2)
        assert_that(refresh_result).is_instance_of(Err)
        assert_that(refresh_result.err_value).is_instance_of(JWTDecodeException)


async def test_refresh_fail_when_refresh_token_expired():
    with patch(
        target="core.util.jwt.JWTUtil.decode", side_effect=[JWTExpiredException(), JWTExpiredException()]
    ) as decode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        refresh_result = jwt_service.refresh(
            access_token="access_token",
            refresh_token="refresh_token",
        )

        assert_that(decode.call_count).is_same_as(2)
        assert_that(refresh_result).is_instance_of(Err)
        assert_that(refresh_result.err_value).is_instance_of(JWTExpiredException)


async def test_refresh_fail_when_raw_access_token_has_not_external_id():
    with patch(target="core.util.jwt.JWTUtil.decode", side_effect=[JWTExpiredException(), {}, {}]) as decode:
        jwt_util = JWTUtil(secret_key="", algorithm="")
        jwt_service = JWTService(
            jwt_util=jwt_util,
        )
        refresh_result = jwt_service.refresh(
            access_token="access_token",
            refresh_token="refresh_token",
        )

        assert_that(decode.call_count).is_same_as(3)
        assert_that(refresh_result).is_instance_of(Err)
        assert_that(refresh_result.err_value).is_instance_of(JWTDecodeException)
