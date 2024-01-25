from http import HTTPStatus

from assertpy import assert_that
from domain.datasource.answer import AnswerModel
from domain.datasource.question import QuestionModel
from domain.datasource.user import UserModel
from domain.service.jwt import JWTSchema
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_delete_all(
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
    await session.commit()
    answer_model1 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
        ]
    )
    await session.commit()

    response = await client.post(
        url=f"/delete-all",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)

    scalar_result = await session.scalars(select(AnswerModel))
    result = scalar_result.all()

    assert_that(result).is_length(2)
    assert_that(result[0].delete_datetime).is_not_none()
    assert_that(result[1].delete_datetime).is_not_none()


async def test_delete_all_only_specific_user(
    client: AsyncClient,
    session: AsyncSession,
    jwt_schema: JWTSchema,
    user_model: UserModel,
):
    user_model2 = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model2,
            question_model,
        ]
    )
    await session.commit()
    answer_model1 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    answer_model3 = AnswerModel(
        question=question_model,
        user=user_model2,
        answer="",
    )
    answer_model4 = AnswerModel(
        question=question_model,
        user=user_model2,
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            answer_model3,
            answer_model4,
        ]
    )
    await session.commit()

    response = await client.post(
        url=f"/delete-all",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)

    scalar_result = await session.scalars(select(AnswerModel).where(AnswerModel.user_id == user_model.id))
    result = scalar_result.all()

    assert_that(result).is_length(2)
    assert_that(result[0].delete_datetime).is_not_none()
    assert_that(result[1].delete_datetime).is_not_none()

    scalar_result = await session.scalars(select(AnswerModel).where(AnswerModel.user_id == user_model2.id))
    result = scalar_result.all()

    assert_that(result).is_length(2)
    assert_that(result[0].delete_datetime).is_none()
    assert_that(result[1].delete_datetime).is_none()
