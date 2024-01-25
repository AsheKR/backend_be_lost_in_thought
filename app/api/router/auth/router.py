from api.router.auth.exception import AuthFailException, JWTDecodeAPIException, JWTExpiredAPIException
from api.router.auth.request import LoginRequest, RefreshRequest
from api.router.auth.response import LoginResponse
from api.router.auth.string import AuthEndPoint
from api.router.depdendency import get_jwt_service, get_user_service
from api.util import AuthorizationCredential
from core.config import get_config
from core.db.session import get_session
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from domain.repository.user import UserRepository
from domain.service.jwt import JWTSchema, JWTService
from domain.service.user import UserService
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from result import Err
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()


@auth_router.post(path=AuthEndPoint.login)
async def login(
    request: LoginRequest,
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
) -> LoginResponse:
    user_schema = await user_service.find_first_by_external_id(external_id=str(request.id))
    if not user_schema:
        raise AuthFailException

    jwt_schema = jwt_service.create(external_id=str(user_schema.external_id))
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )


@auth_router.post(path=AuthEndPoint.refresh)
async def refresh(
    request: RefreshRequest,
    credential: HTTPAuthorizationCredentials = Depends(AuthorizationCredential(auto_error=True)),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> LoginResponse:
    jwt_schema_result = jwt_service.refresh(
        access_token=credential.credentials,
        refresh_token=request.refresh_token,
    )
    match jwt_schema_result:
        case Err(exception):
            match exception:
                case JWTDecodeException():
                    raise JWTDecodeAPIException
                case JWTExpiredException():
                    raise JWTExpiredAPIException
    jwt_schema: JWTSchema = jwt_schema_result.ok_value
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )
