from typing import TYPE_CHECKING, List

from core.db.model import BaseModel
from domain.datasource.language import LanguageModel
from domain.string import TableName
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from domain.datasource.answer import AnswerModel


class QuestionModel(BaseModel):
    __tablename__ = TableName.question

    answer_count: Mapped[int] = mapped_column(default=0, server_default=text("0"), nullable=False)
    translation_list: Mapped[List["QuestionTranslationModel"]] = relationship(back_populates="question")
    answer_list: Mapped[List["AnswerModel"]] = relationship(back_populates="question")


class QuestionTranslationModel(BaseModel):
    __tablename__ = TableName.question_translation

    text: Mapped[str] = mapped_column(nullable=False)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="translation_list")

    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    language: Mapped["LanguageModel"] = relationship(back_populates="translation_question_list")
