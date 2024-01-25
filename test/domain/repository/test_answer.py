from datetime import datetime

from assertpy import assert_that
from domain.datasource.answer import AnswerModel
from domain.datasource.question import QuestionModel
from domain.datasource.user import UserModel
from domain.repository.answer import AnswerRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_answer_pagination(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    question_model = QuestionModel()
    user_model = UserModel()
    session.add_all(
        instances=[
            question_model,
            user_model,
        ],
    )
    await session.flush()
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
        user=user_model,
        answer="",
    )
    answer_model4 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    answer_model5 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    answer_model6 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
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

    answer_list = await answer_repository.list(
        question_external_id=question_model.external_id,
        user_id=user_model.id,
        limit=2,
        offset=0,
    )
    assert_that(answer_list).is_length(2)
    assert_that(answer_list[0].id).is_equal_to(answer_model1.id)
    assert_that(answer_list[1].id).is_equal_to(answer_model2.id)

    answer_list = await answer_repository.list(
        question_external_id=question_model.external_id,
        user_id=user_model.id,
        limit=2,
        offset=2,
    )
    assert_that(answer_list).is_length(2)
    assert_that(answer_list[0].id).is_equal_to(answer_model3.id)
    assert_that(answer_list[1].id).is_equal_to(answer_model4.id)

    answer_list = await answer_repository.list(
        question_external_id=question_model.external_id,
        user_id=user_model.id,
        limit=2,
        offset=4,
    )
    assert_that(answer_list).is_length(2)
    assert_that(answer_list[0].id).is_equal_to(answer_model5.id)
    assert_that(answer_list[1].id).is_equal_to(answer_model6.id)

    answer_list = await answer_repository.list(
        question_external_id=question_model.external_id,
        user_id=user_model.id,
        limit=2,
        offset=6,
    )
    assert_that(answer_list).is_length(0)


async def test_answer_list_exclude_deleted(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    question_model = QuestionModel()
    user_model = UserModel()
    session.add_all(
        instances=[
            question_model,
            user_model,
        ],
    )
    await session.flush()
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
        user=user_model,
        delete_datetime=datetime.now(),
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            answer_model3,
        ]
    )
    await session.commit()

    answer_list = await answer_repository.list(
        question_external_id=question_model.external_id,
        user_id=user_model.id,
        limit=3,
        offset=0,
    )
    assert_that(answer_list).is_length(2)
    assert_that(answer_list[0].id).is_equal_to(answer_model1.id)
    assert_that(answer_list[1].id).is_equal_to(answer_model2.id)


async def test_add(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    user_model = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question_id=question_model.id,
        user_id=user_model.id,
        answer="",
    )
    await answer_repository.add(answer_model=answer_model)
    await session.commit()

    result = await session.scalar(select(AnswerModel).where(AnswerModel.id == answer_model.id))

    assert_that(result).is_not_none()


async def test_edit(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    user_model = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    session.add(
        instance=answer_model,
    )
    await session.commit()
    await answer_repository.edit(answer_model=answer_model, answer="changed")
    await session.commit()

    result = await session.scalar(select(AnswerModel))

    assert_that(result).is_not_none()
    assert_that(result.answer).is_equal_to("changed")


async def test_delete(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    user_model = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model,
            question_model,
        ]
    )
    await session.commit()
    answer_model = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    session.add(
        instance=answer_model,
    )
    await session.commit()
    await answer_repository.delete(
        answer_model=answer_model,
    )
    await session.commit()

    result = await session.scalar(select(AnswerModel).where(AnswerModel.id == answer_model.id))

    assert_that(result).is_not_none()
    assert_that(result.delete_datetime).is_not_none()


async def test_delete_all(session: AsyncSession):
    answer_repository = AnswerRepository(session=session)
    user_model = UserModel()
    question_model = QuestionModel()
    session.add_all(
        instances=[
            user_model,
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
        ],
    )
    await session.commit()
    await answer_repository.delete_all(
        user_id=user_model.id,
    )
    await session.commit()

    scalar_result = await session.scalars(select(AnswerModel).where(AnswerModel.user_id == user_model.id))
    result = scalar_result.all()

    assert_that(result).is_length(2)
    assert_that(result[0].delete_datetime).is_not_none()
    assert_that(result[1].delete_datetime).is_not_none()
