from datetime import datetime

from assertpy import assert_that
from core.language import SupportLanguage
from domain.datasource.answer import AnswerModel
from domain.datasource.language import LanguageModel
from domain.datasource.question import QuestionModel, QuestionTranslationModel
from domain.datasource.user import UserModel
from domain.repository.question import QuestionRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_question_recommendation_list_order_by_answer_count_desc(
    session: AsyncSession,
):
    user_model = UserModel()
    question_model1 = QuestionModel()
    question_model2 = QuestionModel(answer_count=1)
    question_model3 = QuestionModel(answer_count=2)
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
            language_model,
        ]
    )
    await session.commit()
    session.add_all(
        instances=[
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model3,
                text="",
            ),
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )

    question_list = await question_repository.recommendation_list(
        language_code=SupportLanguage.en,
        limit=3,
        offset=0,
    )
    assert_that(question_list[0].external_id).is_equal_to(question_model3.external_id)
    assert_that(question_list[1].external_id).is_equal_to(question_model2.external_id)
    assert_that(question_list[2].external_id).is_equal_to(question_model1.external_id)


async def test_get_question_recommendation_list_without_deleted(session: AsyncSession):
    user_model = UserModel()
    question_model1 = QuestionModel(delete_datetime=datetime.now())
    question_model2 = QuestionModel()
    question_model3 = QuestionModel()
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
            language_model,
        ]
    )
    await session.commit()
    session.add_all(
        instances=[
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model3,
                text="",
            ),
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )

    question_list = await question_repository.recommendation_list(
        language_code=SupportLanguage.en,
        limit=3,
        offset=0,
    )
    assert_that(question_list).is_length(2)
    assert_that(question_list[0].external_id).is_equal_to(question_model2.external_id)
    assert_that(question_list[1].external_id).is_equal_to(question_model3.external_id)


async def test_answered_question_list(session: AsyncSession):
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
    answer_model1 = AnswerModel(
        question=question_model1,
        user=user_model,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model2,
        user=user_model,
        answer="",
    )
    answer_model3 = AnswerModel(
        question=question_model3,
        user=user_model,
        answer="",
    )
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model3,
                text="",
            ),
            answer_model1,
            answer_model2,
            answer_model3,
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model.id,
        language_code=SupportLanguage.en,
        start_datetime=answer_model1.create_datetime,
        end_datetime=answer_model3.create_datetime,
        limit=2,
        offset=0,
    )

    assert_that(question_list[0].external_id).is_equal_to(question_model3.external_id)
    assert_that(question_list[1].external_id).is_equal_to(question_model2.external_id)

    question_list = await question_repository.answered_list(
        user_id=user_model.id, language_code=SupportLanguage.en, limit=2, offset=2,
    start_datetime = answer_model1.create_datetime,
    end_datetime = answer_model3.create_datetime,
    )

    assert_that(question_list).is_length(1)
    assert_that(question_list[0].external_id).is_equal_to(question_model1.external_id)

    question_list = await question_repository.answered_list(
        user_id=user_model.id, language_code=SupportLanguage.en, limit=2, offset=4,
    start_datetime = answer_model1.create_datetime,
    end_datetime = answer_model3.create_datetime,
    )

    assert_that(question_list).is_empty()


async def test_answered_question_answer_datetime(session: AsyncSession):
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
    answer_model3 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            QuestionTranslationModel(
                language=language_model,
                question=question_model,
                text="",
            ),
            answer_model1,
            answer_model2,
            answer_model3,
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model.id,
        language_code=SupportLanguage.en,
        start_datetime=answer_model1.create_datetime,
        end_datetime=answer_model3.create_datetime,
        limit=3,
        offset=0
    )

    assert_that(question_list).is_length(3)
    assert_that(question_list[0].answer_datetime).is_equal_to(answer_model3.create_datetime)
    assert_that(question_list[1].answer_datetime).is_equal_to(answer_model3.create_datetime)
    assert_that(question_list[2].answer_datetime).is_equal_to(answer_model3.create_datetime)


async def test_answered_question_answer_count(session: AsyncSession):
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
    answer_model3 = AnswerModel(
        question=question_model,
        user=user_model,
        answer="",
    )
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            QuestionTranslationModel(
                language=language_model,
                question=question_model,
                text="",
            ),
            answer_model1,
            answer_model2,
            answer_model3,
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model.id,
        language_code=SupportLanguage.en,
        start_datetime=answer_model1.create_datetime,
        end_datetime=answer_model3.create_datetime,
        limit=3,
        offset=0
    )

    assert_that(question_list).is_length(3)
    assert_that(question_list[0].answer_count).is_equal_to(3)
    assert_that(question_list[1].answer_count).is_equal_to(3)
    assert_that(question_list[2].answer_count).is_equal_to(3)


async def test_answered_question_list_only_given_user(session: AsyncSession):
    user_model1 = UserModel()
    question_model1 = QuestionModel()
    user_model2 = UserModel()
    question_model2 = QuestionModel()
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            user_model1,
            question_model1,
            user_model2,
            question_model2,
            language_model,
        ]
    )
    await session.commit()
    answer_model1 = AnswerModel(
        question=question_model1,
        user=user_model1,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model2,
        user=user_model2,
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model1.id,
        language_code=SupportLanguage.en,
        start_datetime=answer_model1.create_datetime,
        end_datetime=answer_model2.create_datetime,
        limit=2,
        offset=0,
    )

    assert_that(question_list).is_length(1)
    assert_that(question_list[0].external_id).is_equal_to(question_model1.external_id)


async def test_answered_question_list_exclude_deleted_answer(session: AsyncSession):
    user_model = UserModel()
    question_model1 = QuestionModel()
    question_model2 = QuestionModel()
    question_model3 = QuestionModel()
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
            language_model,
        ]
    )
    await session.commit()
    answer_model1 = AnswerModel(
        question=question_model1,
        user=user_model,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model2,
        user=user_model,
        answer="",
    )
    answer_model3 = AnswerModel(
        question=question_model3,
        user=user_model,
        delete_datetime=datetime.now(),
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            answer_model3,
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model3,
                text="",
            ),
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model.id, language_code=SupportLanguage.en, limit=3, offset=0,
    start_datetime = answer_model1.create_datetime,
    end_datetime = answer_model3.create_datetime,
    )

    assert_that(question_list).is_length(2)
    assert_that(question_list[0].external_id).is_equal_to(question_model2.external_id)
    assert_that(question_list[1].external_id).is_equal_to(question_model1.external_id)


async def test_answered_question_list_include_deleted_question(session: AsyncSession):
    user_model = UserModel()
    question_model1 = QuestionModel()
    question_model2 = QuestionModel()
    question_model3 = QuestionModel(
        delete_datetime=datetime.now(),
    )
    language_model = LanguageModel(
        code=SupportLanguage.en.value,
    )
    session.add_all(
        instances=[
            user_model,
            question_model1,
            question_model2,
            question_model3,
            language_model,
        ]
    )
    await session.commit()
    answer_model1 = AnswerModel(
        question=question_model1,
        user=user_model,
        answer="",
    )
    answer_model2 = AnswerModel(
        question=question_model2,
        user=user_model,
        answer="",
    )
    answer_model3 = AnswerModel(
        question=question_model3,
        user=user_model,
        answer="",
    )
    session.add_all(
        instances=[
            answer_model1,
            answer_model2,
            answer_model3,
            QuestionTranslationModel(
                language=language_model,
                question=question_model1,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model2,
                text="",
            ),
            QuestionTranslationModel(
                language=language_model,
                question=question_model3,
                text="",
            ),
        ]
    )
    await session.commit()

    question_repository = QuestionRepository(
        session=session,
    )
    question_list = await question_repository.answered_list(
        user_id=user_model.id, language_code=SupportLanguage.en, limit=3, offset=0,
    start_datetime = answer_model1.create_datetime,
    end_datetime = answer_model3.create_datetime,
    )

    assert_that(question_list).is_length(3)
    assert_that(question_list[0].external_id).is_equal_to(question_model3.external_id)
    assert_that(question_list[1].external_id).is_equal_to(question_model2.external_id)
    assert_that(question_list[2].external_id).is_equal_to(question_model1.external_id)
