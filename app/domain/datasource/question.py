from typing import TYPE_CHECKING, List

from core.db.model import BaseModel
from domain.datasource.language import LanguageModel
from domain.string import TableName
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from domain.datasource.answer import AnswerModel
    from domain.datasource.user import UserModel


class QuestionModel(BaseModel):
    __tablename__ = TableName.question

    translation_list: Mapped[List["QuestionTranslationModel"]] = relationship(back_populates="question")
    user_seen_list: Mapped[List["SuggestedQuestionModel"]] = relationship(back_populates="question")
    answer_list: Mapped[List["AnswerModel"]] = relationship(back_populates="question")


class QuestionTranslationModel(BaseModel):
    __tablename__ = TableName.question_translation

    text: Mapped[str] = mapped_column(nullable=False)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="translation_list")

    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    language: Mapped["LanguageModel"] = relationship(back_populates="translation_question_list")


class SuggestedQuestionModel(BaseModel):
    __tablename__ = TableName.suggested_question

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="user_seen_list")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="suggested_question_list")
