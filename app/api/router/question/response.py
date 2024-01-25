from pydantic import UUID4, BaseModel


class QuestionResponse(BaseModel):
    id: UUID4
    question: str


class AnsweredQuestionResponse(BaseModel):
    id: UUID4
    question: str
