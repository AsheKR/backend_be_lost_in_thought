from typing import TYPE_CHECKING

from core.db.model import BaseModel
from domain.string import TableName
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from domain.datasource.question import QuestionModel
    from domain.datasource.user import UserModel


class AnswerModel(BaseModel):
    __tablename__ = TableName.answer

    answer: Mapped[str] = mapped_column(nullable=False)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    question: Mapped["QuestionModel"] = relationship(back_populates="answer_list")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["UserModel"] = relationship(back_populates="answer_list")
