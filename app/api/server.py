from typing import AsyncIterator

from contextlib import asynccontextmanager

from api.exception import APIException, APIExceptionSchema
from api.router.answer.router import answer_detail_router, answer_router
from api.router.auth.router import auth_router
from api.router.delete.router import delete_all_router
from api.router.question.router import question_router
from api.router.question.string import QuestionEndPoint
from api.string import APIDocString, RootEndPoint
from core.config import Env, get_config
from core.db.session import db_manager
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    config = get_config()
    db_manager.init(str(config.SQLALCHEMY_DATABASE_URI))
    yield
    await db_manager.close()


def _init_router(fast_api_: FastAPI) -> None:
    question_router.include_router(
        answer_router,
        prefix=f"{QuestionEndPoint.answer}",
    )

    fast_api_.include_router(auth_router, prefix=RootEndPoint.auth)
    fast_api_.include_router(question_router, prefix=RootEndPoint.question)
    fast_api_.include_router(answer_detail_router, prefix=RootEndPoint.answer)
    fast_api_.include_router(delete_all_router, prefix=RootEndPoint.delete_all)


def _init_listener(fast_api_: FastAPI) -> None:
    @fast_api_.exception_handler(APIException)
    async def custom_exception_handler(request: Request, exc: APIException) -> JSONResponse:
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
        title=APIDocString.label,
        description=APIDocString.description,
        version=APIDocString.version,
        docs_url=None if config.ENV == Env.production else RootEndPoint.docs,
        redoc_url=None if config.ENV == Env.production else RootEndPoint.redoc,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    _init_router(fast_api_=fast_api_)
    _init_listener(fast_api_=fast_api_)
    return fast_api_


fast_api = create_fast_api()
