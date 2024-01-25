from typing import Any, Optional

from api.exception import UnauthorizedException, ForbiddenException
from api.router.auth.exception import JWTDecodeAPIException, JWTExpiredAPIException
from core.config import get_config
from core.db.session import get_session
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from domain.repository.user import UserRepository
from domain.service.jwt import JWTService
from domain.service.user import InternalUserSchema, UserService
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from result import Err
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

AuthorizationHeader = APIKeyHeader(name="Authorization", scheme_name="JWT")


class AuthorizationCredential:
    def __init__(self, auto_error: bool = False):
        self._auto_error = auto_error

    def __call__(self, authorization: str = Security(AuthorizationHeader)) -> Optional[HTTPAuthorizationCredentials]:
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self._auto_error:
                raise ForbiddenException
            else:
                return None
        if scheme.lower() != "jwt":
            if self._auto_error:
                raise ForbiddenException
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    credential: Optional[HTTPAuthorizationCredentials] = Depends(AuthorizationCredential(auto_error=True)),
) -> Optional[InternalUserSchema]:
    if not credential:
        return None

    config = get_config()
    jwt_util = JWTUtil(
        secret_key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    jwt_service = JWTService(jwt_util=jwt_util)
    jwt_decode_result = jwt_service.decode_token(
        token=credential.credentials,
    )
    match jwt_decode_result:
        case Err(exception):
            match exception:
                case JWTDecodeException():
                    raise JWTDecodeAPIException
                case JWTExpiredException():
                    raise JWTExpiredAPIException

    claim: dict[str, Any] = jwt_decode_result.ok_value
    external_id = claim["sub"]

    user_repository = UserRepository(session=session)
    user_service = UserService(user_repository=user_repository)
    user_schema = await user_service.find_first_by_external_id(external_id=external_id)
    if not user_schema:
        raise UnauthorizedException

    return user_schema
