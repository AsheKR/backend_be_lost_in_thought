from core.language import SupportLanguage
from domain.datasource.answer import AnswerModel
from domain.datasource.language import LanguageModel
from domain.datasource.question import QuestionModel, QuestionTranslationModel, SuggestedQuestionModel
from domain.repository.base import BaseRepository
from pydantic import UUID4, BaseModel
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce, count


class Question(BaseModel):
    external_id: UUID4
    question: str


class QuestionRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> QuestionModel | None:
        query = select(QuestionModel).where(QuestionModel.external_id == external_id)
        return await self._session.scalar(query)  # type: ignore

    async def answered_list(
        self, user_id: int, language_code: SupportLanguage, limit: int, offset: int
    ) -> list[Question]:
        query = (
            select(AnswerModel, QuestionModel, QuestionTranslationModel)
            .join(
                QuestionModel,
                AnswerModel.question_id == QuestionModel.id,
            )
            .join(
                QuestionTranslationModel,
                QuestionTranslationModel.question_id == QuestionModel.id,
            )
            .join(
                LanguageModel,
                LanguageModel.id == QuestionTranslationModel.language_id,
            )
            .where(
                AnswerModel.delete_datetime == None,
                AnswerModel.user_id == user_id,
                LanguageModel.code == language_code.value,
            )
            .order_by(AnswerModel.id)
            .limit(limit=limit)
            .offset(offset=offset)
        )
        execute_result = await self._session.execute(query)
        result = list(execute_result)

        return [
            Question(
                external_id=element.QuestionModel.external_id,
                question=element.QuestionTranslationModel.text,
            )
            for element in result
        ]

    async def recommendation_list(self, user_id: int, language_code: SupportLanguage, limit: int) -> list[Question]:
        suggested_subquery = (
            select(SuggestedQuestionModel.question_id, count(SuggestedQuestionModel.id).label("suggested_count"))
            .filter(SuggestedQuestionModel.user_id == user_id)
            .group_by(SuggestedQuestionModel.question_id)
            .subquery()
        )

        query = (
            select(  # type: ignore
                QuestionModel,
                QuestionTranslationModel,
                coalesce(suggested_subquery.c.suggested_count, 0).label("suggested_count"),
            )
            .join(
                QuestionTranslationModel,
                QuestionTranslationModel.question_id == QuestionModel.id,
            )
            .join(
                LanguageModel,
                LanguageModel.id == QuestionTranslationModel.language_id,
            )
            .where(
                QuestionModel.delete_datetime == None,
                LanguageModel.code == language_code.value,
            )
            .outerjoin(
                suggested_subquery,
                suggested_subquery.c.question_id == QuestionModel.id,
            )
            .order_by(
                coalesce(suggested_subquery.c.suggested_count, 0),
                QuestionModel.id,
            )
            .limit(limit)
        )
        execute_result = await self._session.execute(query)
        result = list(execute_result)

        self._session.add_all(
            instances=[
                SuggestedQuestionModel(
                    user_id=user_id,
                    question_id=element.QuestionModel.id,
                )
                for element in result
            ]
        )

        return [
            Question(
                external_id=element.QuestionModel.external_id,
                question=element.QuestionTranslationModel.text,
            )
            for element in result
        ]
