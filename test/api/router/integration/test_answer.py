from http import HTTPStatus

from assertpy import assert_that
from core.config import get_config
from core.util.jwt import JWTUtil
from domain.repository.answer import AnswerModel, AnswerRepository
from domain.repository.question import QuestionModel
from domain.repository.user import UserModel
from domain.service.jwt import JWTService
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


async def test_answer_pagination(
    client: AsyncClient,
    session: async_scoped_session[AsyncSession],
):
    question_model = QuestionModel()
    user_model = UserModel()
    session.add_all(
        instances=[
            question_model,
            user_model,
        ]
    )
    answer_model1 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    answer_model2 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    answer_model3 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    answer_model4 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    answer_model5 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    answer_model6 = AnswerModel(
        question=question_model,
        user=user_model,
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            answer_model3,
            answer_model4,
            answer_model5,
            answer_model6,
        ]
    )
    await session.commit()

    config = get_config()
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(answer_model1.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(answer_model2.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2&offset=2",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(answer_model3.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(answer_model4.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2&offset=4",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(answer_model5.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(answer_model6.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2&offset=6",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data).is_length(0)


async def test_add(
    client: AsyncClient,
    session: async_scoped_session[AsyncSession],
):
    user_model = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model,
        ]
    )
    await session.commit()

    config = get_config()
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.post(
        url=f"/question/{question_model.external_id}/answer",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
        json={"answer": "answer"},
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    result = await session.scalar(select(AnswerModel))
    assert_that(result.answer).is_equal_to("answer")


async def test_add_fail_when_question_not_found(
    client: AsyncClient,
    session: async_scoped_session[AsyncSession],
):
    user_model = UserModel()
    session.add_all(
        instances=[
            user_model,
        ]
    )
    await session.commit()

    config = get_config()
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.post(
        url=f"/question/question_id/answer",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
        json={"answer": "answer"},
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.UNPROCESSABLE_ENTITY)
