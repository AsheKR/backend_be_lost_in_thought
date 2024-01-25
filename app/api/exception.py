from enum import StrEnum
from http import HTTPStatus

from pydantic import BaseModel


class ErrorCode(StrEnum):
    auth_fail = "AUTH__FAIL"
    jwt_decode_token = "AUTH__DECODE_TOKEN"
    jwt_expired_token = "AUTH__EXPIRED_TOKEN"


class APIException(Exception):
    status_code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class APIExceptionSchema(BaseModel):
    error_code: str
    message: str


class BadRequestException(APIException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(APIException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(APIException):
    status_code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description
