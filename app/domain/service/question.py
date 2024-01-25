from domain.repository.question import QuestionRepository
from domain.service.base import BaseService
from pydantic import UUID4, BaseModel


class QuestionSchema(BaseModel):
    external_id: UUID4
    question: str


class QuestionService(BaseService):
    def __init__(self, question_repository: QuestionRepository):
        self._question_repository = question_repository

    async def get_question_recommendation_list(self, user_id: int) -> list[QuestionSchema]:
        question_list = await self._question_repository.get_question_recommendation_list(
            user_id=user_id,
            limit=3,
        )

        return [
            QuestionSchema(
                external_id=question.external_id,
                question=question.question,
            )
            for question in question_list
        ]
