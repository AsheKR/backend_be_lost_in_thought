from enum import StrEnum
from http import HTTPStatus

from pydantic import BaseModel


class ErrorCode(StrEnum):
    auth_fail = "AUTH__FAIL"
    jwt_decode_token = "AUTH__DECODE_TOKEN"
    jwt_expired_token = "AUTH__EXPIRED_TOKEN"


class APIException(Exception):
    status_code: int = HTTPStatus.BAD_GATEWAY.value
    error_code: str = HTTPStatus.BAD_GATEWAY.phrase
    message: str = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class APIExceptionSchema(BaseModel):
    error_code: str
    message: str


class BadRequestException(APIException):
    status_code = HTTPStatus.BAD_REQUEST.value
    error_code = HTTPStatus.BAD_REQUEST.phrase
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(APIException):
    status_code = HTTPStatus.NOT_FOUND.value
    error_code = HTTPStatus.NOT_FOUND.phrase
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(APIException):
    status_code = HTTPStatus.FORBIDDEN.value
    error_code = HTTPStatus.FORBIDDEN.phrase
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED.value
    error_code = HTTPStatus.UNAUTHORIZED.phrase
    message = HTTPStatus.UNAUTHORIZED.description
