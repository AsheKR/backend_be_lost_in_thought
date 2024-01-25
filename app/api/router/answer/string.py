from enum import StrEnum


class AnswerEndPoint(StrEnum):
    list = ""
    add = ""
    edit = "/{answer_id}"
