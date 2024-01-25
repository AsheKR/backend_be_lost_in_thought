from api.router.user import user_router
from api.string import APIDocString, EndPoint
from core.config import Env, get_config
from fastapi import FastAPI


def _init_router(app: FastAPI):
    app.include_router(user_router, prefix=EndPoint.user)


def create_fast_api() -> FastAPI:
    config = get_config()

    app_ = FastAPI(
        title=APIDocString.title,
        description=APIDocString.description,
        version=APIDocString.version,
        docs_url=None if config.ENV == Env.production else EndPoint.docs,
        redoc_url=None if config.ENV == Env.production else EndPoint.redoc,
    )
    _init_router(app=app_)
    return app_


fast_api = create_fast_api()
