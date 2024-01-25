from datetime import datetime

from core.language import SupportLanguage
from domain.datasource.answer import AnswerModel
from domain.datasource.language import LanguageModel
from domain.datasource.question import QuestionModel, QuestionTranslationModel
from domain.repository.base import BaseRepository
from pydantic import UUID4, BaseModel
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce, count


class AnsweredQuestion(BaseModel):
    external_id: UUID4
    question: str
    answer_count: int
    answer_datetime: datetime


class RecommendationQuestion(BaseModel):
    external_id: UUID4
    question: str


class QuestionRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> QuestionModel | None:
        query = select(QuestionModel).where(QuestionModel.external_id == external_id)
        return await self._session.scalar(query)  # type: ignore

    async def answered_list(
        self,
            user_id: int,
            language_code: SupportLanguage,
            start_datetime: datetime,
            end_datetime: datetime,
            limit: int,
            offset: int,
    ) -> list[AnsweredQuestion]:
        answered_subquery = (
            select(
                AnswerModel.question_id,
                count(AnswerModel.id).label("answer_count"),
            )
            .filter(
                AnswerModel.delete_datetime == None,
                AnswerModel.user_id == user_id,
                LanguageModel.code == language_code.value,
            )
            .group_by(AnswerModel.question_id)
            .subquery()
        )
        query = (
            select(
                AnswerModel,
                QuestionModel,
                QuestionTranslationModel,
                coalesce(answered_subquery.c.answer_count, 0).label("answer_count"),
            )
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
            .outerjoin(
                answered_subquery,
                answered_subquery.c.question_id == QuestionModel.id,
            )
            .where(
                AnswerModel.delete_datetime == None,
                AnswerModel.user_id == user_id,
                LanguageModel.code == language_code.value,
                AnswerModel.create_datetime >= start_datetime,
                AnswerModel.create_datetime <= end_datetime,
            )
            .order_by(AnswerModel.create_datetime.desc())
            .limit(limit=limit)
            .offset(offset=offset)
        )
        execute_result = await self._session.execute(query)
        result = list(execute_result)

        return [
            AnsweredQuestion(
                external_id=element.QuestionModel.external_id,
                question=element.QuestionTranslationModel.text,
                answer_count=element.answer_count,
                answer_datetime=element.AnswerModel.create_datetime,
            )
            for element in result
        ]

    async def recommendation_list(self, language_code: SupportLanguage, limit: int, offset: int) -> list[RecommendationQuestion]:
        query = (
            select(  # type: ignore
                QuestionModel,
                QuestionTranslationModel,
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
            .order_by(
                QuestionModel.answer_count.desc(),
                QuestionModel.id,
            )
            .limit(limit)
            .offset(offset)
        )
        execute_result = await self._session.execute(query)
        result = list(execute_result)

        return [
            RecommendationQuestion(
                external_id=element.QuestionModel.external_id,
                question=element.QuestionTranslationModel.text,
            )
            for element in result
        ]
