from pydantic import UUID4, BaseModel


class QuestionResponse(BaseModel):
    external_id: UUID4
    question: str
