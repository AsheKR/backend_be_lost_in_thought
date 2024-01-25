from enum import StrEnum


class AnswerEndPoint(StrEnum):
    list = ""
    add = ""


class AnswerDetailEndPoint(StrEnum):
    edit = "/{answer_id}"
    delete = "/{answer_id}"
