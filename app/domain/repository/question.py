from domain.datasource.question import QuestionModel, SuggestedQuestionModel
from domain.repository.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce, count


class QuestionRepository(BaseRepository):
    async def find_first_by_external_id(self, external_id: str) -> QuestionModel | None:
        query = select(QuestionModel).where(QuestionModel.external_id == external_id)
        return await self._session.scalar(query)  # type: ignore

    async def recommendation_list(self, user_id: int, limit: int) -> list[QuestionModel]:
        suggested_subquery = (
            select(SuggestedQuestionModel.question_id, count(SuggestedQuestionModel.id).label("suggested_count"))
            .filter(SuggestedQuestionModel.user_id == user_id)
            .group_by(SuggestedQuestionModel.question_id)
            .subquery()
        )

        query = (
            select(  # type: ignore
                QuestionModel,
                coalesce(suggested_subquery.c.suggested_count, 0).label("suggested_count"),
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
        scalarResult = await self._session.scalars(query)
        result = scalarResult.all()

        self._session.add_all(
            instances=[
                SuggestedQuestionModel(
                    user_id=user_id,
                    question_id=question.id,
                )
                for question in result
            ]
        )

        return result  # type: ignore
