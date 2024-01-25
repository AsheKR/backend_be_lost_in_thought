from pydantic import UUID4, BaseModel


class AddAnswerRequest(BaseModel):
    answer: str
