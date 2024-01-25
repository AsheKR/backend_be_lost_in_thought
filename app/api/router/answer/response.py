from datetime import datetime

from pydantic import UUID4, BaseModel


class AnswerResponse(BaseModel):
    id: UUID4
    answer: str
    create_datetime: datetime
