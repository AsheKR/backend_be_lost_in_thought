from typing import TYPE_CHECKING, List

from core.db.model import BaseModel
from core.language import SupportLanguage
from domain.string import TableName
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from domain.datasource.question import QuestionTranslationModel


class LanguageModel(BaseModel):
    __tablename__ = TableName.language

    code: Mapped[str] = mapped_column(nullable=False)

    translation_question_list: Mapped[List["QuestionTranslationModel"]] = relationship(back_populates="language")
