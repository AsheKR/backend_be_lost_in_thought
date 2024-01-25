from api.router.auth.exception import AuthFailException, JWTDecodeTokenAPIException, JWTExpiredTokenAPIException
from api.router.auth.request import LoginRequest, RefreshRequest
from api.router.auth.response import LoginResponse
from api.router.auth.security import AuthorizationHeader
from api.string import EndPoint
from core.util.jwt import JWTDecodeException, JWTExpiredException
from domain.service.jwt import JWTSchema, JWTService
from domain.service.user import UserService
from fastapi import APIRouter
from result import Err

auth_router = APIRouter()


@auth_router.post(path=EndPoint.login)
async def login(request: LoginRequest) -> LoginResponse:
    user_schema = await UserService().find_first_by_external_id(external_id=str(request.external_id))
    if not user_schema:
        raise AuthFailException

    jwt_schema = JWTService().create(external_id=str(user_schema.external_id))
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )


@auth_router.post(path=EndPoint.refresh)
def refresh(request: RefreshRequest, access_token: str = AuthorizationHeader) -> LoginResponse:
    jwt_scheme_result = JWTService().refresh(
        access_token=access_token,
        refresh_token=request.refresh_token,
    )
    match jwt_scheme_result:
        case Err(exception):
            match exception:
                case JWTDecodeException():
                    raise JWTDecodeTokenAPIException
                case JWTExpiredException():
                    raise JWTExpiredTokenAPIException
    jwt_schema: JWTSchema = jwt_scheme_result.ok_value
    return LoginResponse(
        access_token=jwt_schema.access_token,
        refresh_token=jwt_schema.refresh_token,
    )
