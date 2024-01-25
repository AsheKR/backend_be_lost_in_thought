from typing import TYPE_CHECKING

from core.db.model import BaseModel
from domain.repository.base import BaseRepository
from domain.string import TableName
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import coalesce, count

if TYPE_CHECKING:
    from domain.repository.user import UserModel


class QuestionModel(BaseModel):
    __tablename__ = TableName.question

    question: Mapped[str] = mapped_column(nullable=False, default="")

    user_seen_list: Mapped["SuggestedQuestionModel"] = relationship(back_populates="question")


class SuggestedQuestionModel(BaseModel):
    __tablename__ = TableName.suggested_question

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="user_seen_list")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="suggested_question_list")


class QuestionRepository(BaseRepository):
    async def get_question_recommendation_list(self, user_id: int, limit: int) -> list[QuestionModel]:
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
