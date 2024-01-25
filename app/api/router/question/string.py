from enum import StrEnum


class QuestionEndPoint(StrEnum):
    answer = "/{question_id}/answer"
    recommendation = "/recommendation"
