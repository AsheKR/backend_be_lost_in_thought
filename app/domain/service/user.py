from domain.repository.user import UserModel, UserRepository
from domain.service.base import BaseService
from sqlalchemy.orm import Session


class UserService(BaseService):
    def __init__(self, session: Session, user_repository: UserRepository):
        super().__init__(session=session)
        self._user_repository = user_repository

    def create_user(self) -> None:
        self._user_repository.add(user=UserModel())
