from typing import Any

from datetime import datetime, timedelta
from enum import StrEnum

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
    def __init__(self, secret_key: str, algorithm: str):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, subject: str, expire_delta: timedelta) -> str:
        expire = datetime.utcnow() + expire_delta
        to_encode = {
            JWTKey.expire: expire,
            JWTKey.subject: subject,
        }
        return jwt.encode(  # type: ignore
            claims=to_encode,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str, verify_exp: bool = True) -> dict[str, Any]:
        try:
            return jwt.decode(  # type: ignore
                token=token,
                key=self._secret_key,
                algorithms=self._algorithm,
                options={"verify_exp": verify_exp},
            )
        except ExpiredSignatureError:
            raise JWTExpiredException
        except JWTError:
            raise JWTDecodeException
