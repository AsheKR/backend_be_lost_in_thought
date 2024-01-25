from http import HTTPStatus

from assertpy import assert_that
from core.config import get_config
from core.util.jwt import JWTUtil
from domain.repository.answer import AnswerModel
from domain.repository.question import QuestionModel
from domain.repository.user import UserModel
from domain.service.jwt import JWTSchema, JWTService
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_answer_pagination(
    client: AsyncClient,
    session: AsyncSession,
    jwt_schema: JWTSchema,
    user_model: UserModel,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
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

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["id"]).is_equal_to(str(answer_model1.external_id))
    assert_that(response_data[1]["id"]).is_equal_to(str(answer_model2.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2&offset=2",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["id"]).is_equal_to(str(answer_model3.external_id))
    assert_that(response_data[1]["id"]).is_equal_to(str(answer_model4.external_id))

    response = await client.get(
        url=f"/question/{question_model.external_id}/answer?limit=2&offset=4",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["id"]).is_equal_to(str(answer_model5.external_id))
    assert_that(response_data[1]["id"]).is_equal_to(str(answer_model6.external_id))

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
    session: AsyncSession,
    jwt_schema: JWTSchema,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
        ]
    )
    await session.commit()

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
    jwt_schema: JWTSchema,
):
    response = await client.post(
        url=f"/question/question_id/answer",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
        json={"answer": "answer"},
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.UNPROCESSABLE_ENTITY)


async def test_edit(
    client: AsyncClient,
    session: AsyncSession,
    user_model: UserModel,
    jwt_schema: JWTSchema,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question=question_model,
        user=user_model,
    )
    session.add(
        instance=answer_model,
    )
    await session.commit()

    response = await client.patch(
        url=f"/answer/{answer_model.external_id}",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
        json={
            "answer": "changed",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    result = await session.scalar(select(AnswerModel))
    assert_that(result).is_not_none()
    assert_that(result.answer).is_equal_to("changed")


async def test_edit_fail_when_answer_not_found(
    client: AsyncClient,
    session: AsyncSession,
    jwt_schema: JWTSchema,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
        ]
    )
    await session.commit()

    response = await client.patch(
        url=f"/answer/answer_id",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
        json={
            "answer": "changed",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.UNPROCESSABLE_ENTITY)


async def test_delete(
    client: AsyncClient,
    session: AsyncSession,
    user_model: UserModel,
    jwt_schema: JWTSchema,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question=question_model,
        user=user_model,
    )
    session.add(
        instance=answer_model,
    )
    await session.commit()

    response = await client.delete(
        url=f"/answer/{answer_model.external_id}",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    result = await session.scalar(select(AnswerModel))
    assert_that(result).is_not_none()
    assert_that(result.delete_datetime).is_not_none()


async def test_delete_fail_when_answer_not_found(
    client: AsyncClient,
    session: AsyncSession,
    user_model: UserModel,
    jwt_schema: JWTSchema,
):
    question_model = QuestionModel()
    session.add_all(
        instances=[
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question=question_model,
        user=user_model,
    )
    session.add(
        instance=answer_model,
    )
    await session.commit()

    response = await client.delete(
        url=f"/answer/answer_id",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.UNPROCESSABLE_ENTITY)
