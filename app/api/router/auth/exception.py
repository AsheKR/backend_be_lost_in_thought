from api.exception import BadRequestException, ErrorCode


class AuthFailException(BadRequestException):
    error_code = ErrorCode.auth_fail.value


class JWTDecodeTokenAPIException(AuthFailException):
    error_code = ErrorCode.jwt_decode_token.value


class JWTExpiredTokenAPIException(AuthFailException):
    error_code = ErrorCode.jwt_expired_token.value
