from sqlalchemy.orm import Session


class BaseSessionMixin:
    def __init__(self, session: Session):
        self._session = session
