from datetime import datetime, timedelta
from enum import StrEnum

from core.config import get_config
from jose import ExpiredSignatureError, JWTError, jwt


class JWTKey(StrEnum):
    expire = "exp"
    subject = "sub"


class JWTException(Exception):
    pass


class JWTExpiredException(JWTException):
    pass


class JWTDecodeException(JWTException):
    pass


class JWTUtil:
    @staticmethod
    def encode(subject: str, expire_delta: timedelta, **kwargs) -> str:
        config = get_config()
        expire = datetime.utcnow() + expire_delta
        to_encode = {
            **kwargs,
            JWTKey.expire: expire,
            JWTKey.subject: subject,
        }
        return jwt.encode(
            claims=to_encode,
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )

    @staticmethod
    def decode(token: str, verify_exp: bool = True) -> dict:
        config = get_config()
        try:
            return jwt.decode(
                token=token,
                key=config.JWT_SECRET_KEY,
                algorithms=config.JWT_ALGORITHM,
                options={"verify_exp": verify_exp},
            )
        except ExpiredSignatureError:
            raise JWTExpiredException
        except JWTError:
            raise JWTDecodeException
