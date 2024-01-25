from api.exception import BadRequestException, ErrorCode


class AuthFailException(BadRequestException):
    error_code = ErrorCode.auth_fail.value


class JWTDecodeAPIException(AuthFailException):
    error_code = ErrorCode.jwt_decode_token.value


class JWTExpiredAPIException(AuthFailException):
    error_code = ErrorCode.jwt_expired_token.value
