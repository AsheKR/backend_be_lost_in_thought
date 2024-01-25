from datetime import datetime, timedelta

from assertpy import assert_that, fail
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from freezegun import freeze_time


async def test_encode_and_decode():
    jwt_util = JWTUtil(
        secret_key="secret_key",
        algorithm="HS256",
    )

    token = jwt_util.encode(
        subject="subject",
        expire_delta=timedelta(days=1),
        id="id",
    )

    original = jwt_util.decode(
        token=token,
    )

    assert_that(original.get("sub")).is_equal_to("subject")
    assert_that(original.get("id")).is_equal_to("id")


async def test_decode_fail_when_expired_signature_error():
    jwt_util = JWTUtil(
        secret_key="secret_key",
        algorithm="HS256",
    )

    token = jwt_util.encode(
        subject="subject",
        expire_delta=timedelta(),
        id="id",
    )

    with freeze_time(datetime.utcnow() + timedelta(days=1)):
        try:
            jwt_util.decode(token=token)
        except JWTExpiredException:
            pass
        else:
            fail()


async def test_decode_with_ignore_expired():
    jwt_util = JWTUtil(
        secret_key="secret_key",
        algorithm="HS256",
    )

    token = jwt_util.encode(
        subject="subject",
        expire_delta=timedelta(),
        id="id",
    )

    with freeze_time(datetime.utcnow() + timedelta(days=1)):
        jwt_util.decode(
            token=token,
            verify_exp=False,
        )


async def test_decode_fail_when_jwt_error():
    jwt_util = JWTUtil(
        secret_key="secret_key",
        algorithm="HS256",
    )

    try:
        jwt_util.decode(token="token")
    except JWTDecodeException:
        pass
    else:
        fail()
