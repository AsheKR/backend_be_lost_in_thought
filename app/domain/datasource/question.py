from typing import TYPE_CHECKING

from core.db.model import BaseModel
from domain.string import TableName
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from domain.datasource.answer import AnswerModel
    from domain.datasource.user import UserModel


class QuestionModel(BaseModel):
    __tablename__ = TableName.question

    question: Mapped[str] = mapped_column(nullable=False, default="")

    user_seen_list: Mapped["SuggestedQuestionModel"] = relationship(back_populates="question")
    answer_list: Mapped["AnswerModel"] = relationship(back_populates="question")


class SuggestedQuestionModel(BaseModel):
    __tablename__ = TableName.suggested_question

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="user_seen_list")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="suggested_question_list")
