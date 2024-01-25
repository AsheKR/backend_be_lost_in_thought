from assertpy import assert_that
from domain.datasource.question import QuestionModel
from domain.datasource.user import UserModel
from domain.repository.question import QuestionRepository, SuggestedQuestionModel
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


async def test_get_question_recommendation_list_order_by_suggested_count_asc(
    session: AsyncSession,
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

    question_respository = QuestionRepository(
        session=session,
    )

    question_list = await question_respository.recommendation_list(
        user_id=user_model.id,
        limit=3,
    )
    assert_that(question_list[0].id).is_equal_to(question_model3.id)
    assert_that(question_list[1].id).is_equal_to(question_model2.id)
    assert_that(question_list[2].id).is_equal_to(question_model1.id)


async def test_get_question_recommendation_list_rotation(session: AsyncSession):
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

    question_respository = QuestionRepository(
        session=session,
    )

    question_list = await question_respository.recommendation_list(
        user_id=user_model.id,
        limit=3,
    )
    await session.commit()

    assert_that(question_list[0].id).is_equal_to(question_model1.id)
    assert_that(question_list[1].id).is_equal_to(question_model2.id)
    assert_that(question_list[2].id).is_equal_to(question_model3.id)

    question_list = await question_respository.recommendation_list(
        user_id=user_model.id,
        limit=3,
    )
    await session.commit()

    assert_that(question_list[0].id).is_equal_to(question_model4.id)
    assert_that(question_list[1].id).is_equal_to(question_model5.id)
    assert_that(question_list[2].id).is_equal_to(question_model6.id)

    question_list = await question_respository.recommendation_list(
        user_id=user_model.id,
        limit=3,
    )
    await session.commit()

    assert_that(question_list[0].id).is_equal_to(question_model1.id)
    assert_that(question_list[1].id).is_equal_to(question_model2.id)
    assert_that(question_list[2].id).is_equal_to(question_model3.id)
