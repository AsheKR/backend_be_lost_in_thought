from api.exception import APIException, APIExceptionSchema
from api.router.auth.router import auth_router
from api.string import APIDocString, EndPoint
from core.config import Env, get_config
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse


def _init_router(fast_api_: FastAPI):
    fast_api_.include_router(auth_router, prefix=EndPoint.auth)


def _init_listener(fast_api_: FastAPI):
    @fast_api_.exception_handler(APIException)
    async def custom_exception_handler(request: Request, exc: APIException):
        return ORJSONResponse(
            status_code=exc.status_code,
            content=APIExceptionSchema(
                error_code=exc.error_code,
                message=exc.message,
            ).model_dump(),
        )


def create_fast_api() -> FastAPI:
    config = get_config()

    fast_api_ = FastAPI(
        title=APIDocString.title,
        description=APIDocString.description,
        version=APIDocString.version,
        docs_url=None if config.ENV == Env.production else EndPoint.docs,
        redoc_url=None if config.ENV == Env.production else EndPoint.redoc,
        default_response_class=ORJSONResponse,
    )
    _init_router(fast_api_=fast_api_)
    _init_listener(fast_api_=fast_api_)
    return fast_api_


fast_api = create_fast_api()
