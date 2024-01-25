from http import HTTPStatus

from assertpy import assert_that
from core.config import get_config
from core.util.jwt import JWTUtil
from domain.repository.question import QuestionModel, SuggestedQuestionModel
from domain.repository.user import UserModel
from domain.service.jwt import JWTService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


async def test_recommendation_list_order_by_suggested_count_asc(
    client: AsyncClient, session: async_scoped_session[AsyncSession]
):
    user_model = UserModel()
    question_model1 = QuestionModel()
    question_model2 = QuestionModel()
    question_model3 = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
        ]
    )
    await session.commit()
    session.add_all(
        instances=[
            SuggestedQuestionModel(question_id=question_model1.id, user_id=user_model.id),
            SuggestedQuestionModel(question_id=question_model1.id, user_id=user_model.id),
            SuggestedQuestionModel(question_id=question_model2.id, user_id=user_model.id),
        ]
    )
    await session.commit()

    config = get_config()
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.get(
        url="/question/recommendation",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(question_model3.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(question_model2.external_id))
    assert_that(response_data[2]["external_id"]).is_equal_to(str(question_model1.external_id))


async def test_recommendation_list_rotation(client: AsyncClient, session: async_scoped_session[AsyncSession]):
    user_model = UserModel()
    question_model1 = QuestionModel()
    question_model2 = QuestionModel()
    question_model3 = QuestionModel()
    question_model4 = QuestionModel()
    question_model5 = QuestionModel()
    question_model6 = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
            question_model4,
            question_model5,
            question_model6,
        ]
    )
    await session.commit()

    config = get_config()
    jwt_util = JWTUtil(secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    jwt_schema = JWTService(jwt_util=jwt_util).create(external_id=str(user_model.external_id))

    response = await client.get(
        url="/question/recommendation",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(question_model1.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(question_model2.external_id))
    assert_that(response_data[2]["external_id"]).is_equal_to(str(question_model3.external_id))

    response = await client.get(
        url="/question/recommendation",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(question_model4.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(question_model5.external_id))
    assert_that(response_data[2]["external_id"]).is_equal_to(str(question_model6.external_id))

    response = await client.get(
        url="/question/recommendation",
        headers={
            "Authorization": f"JWT {jwt_schema.access_token}",
        },
    )

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    response_data = response.json()
    assert_that(response_data[0]["external_id"]).is_equal_to(str(question_model1.external_id))
    assert_that(response_data[1]["external_id"]).is_equal_to(str(question_model2.external_id))
    assert_that(response_data[2]["external_id"]).is_equal_to(str(question_model3.external_id))
