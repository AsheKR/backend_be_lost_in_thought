from fastapi import FastAPI

from core.config import Env, get_config


def create_fast_api() -> FastAPI:
    config = get_config()
    app_ = FastAPI(
        title="backend",
        description="backend API",
        version="0.0.1",
        docs_url=None if config.ENV == Env.production else "/docs",
        redoc_url=None if config.ENV == Env.production else "/redoc",
    )
    return app_


fast_api = create_fast_api()
