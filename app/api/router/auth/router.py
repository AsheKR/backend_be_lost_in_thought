from fastapi.security import HTTPAuthorizationCredentials
from api.router.auth.exception import AuthFailException, JWTDecodeAPIException, JWTExpiredAPIException
from api.router.auth.request import LoginRequest, RefreshRequest
from api.router.auth.response import LoginResponse
from api.router.auth.security import AuthorizationHeader, get_authorization_credential
from api.string import EndPoint
from core.config import get_config
from core.db.session import get_session
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from domain.repository.user import UserRepository
from domain.service.jwt import JWTSchema, JWTService
from domain.service.user import UserService
from fastapi import APIRouter, Depends, Security
from result import Err

auth_router = APIRouter()


def _get_jwt_util() -> JWTUtil:
    config = get_config()
    return JWTUtil(
        secret_key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )


@auth_router.post(path=EndPoint.login)
async def login(request: LoginRequest) -> LoginResponse:
    session = get_session()
    user_repository = UserRepository(
        session=session,
    )
    user_schema = await UserService(
        user_repository=user_repository,
    ).find_first_by_external_id(external_id=str(request.external_id))
    if not user_schema:
        raise AuthFailException

    jwt_util = _get_jwt_util()
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_schema.external_id))
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )


@auth_router.post(path=EndPoint.refresh)
async def refresh(request: RefreshRequest, credential: HTTPAuthorizationCredentials = Depends(get_authorization_credential)) -> LoginResponse:
    jwt_util = _get_jwt_util()
    jwt_scheme_result = JWTService(
        jwt_util=jwt_util,
    ).refresh(
        access_token=credential.credentials,
        refresh_token=request.refresh_token,
    )
    match jwt_scheme_result:
        case Err(exception):
            match exception:
                case JWTDecodeException():
                    raise JWTDecodeAPIException
                case JWTExpiredException():
                    raise JWTExpiredAPIException
    jwt_schema: JWTSchema = jwt_scheme_result.ok_value
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )
