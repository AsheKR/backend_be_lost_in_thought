from pydantic import UUID4, BaseModel


class AnswerResponse(BaseModel):
    external_id: UUID4
    answer: str
