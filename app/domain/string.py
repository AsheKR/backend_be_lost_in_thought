from enum import StrEnum


class TableName(StrEnum):
    user = "user"
    question = "question"
    question_translation = "question_translation"
    suggested_question = "suggested_question"
    answer = "answer"
    language = "language"
