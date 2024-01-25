from core.db.session import session
from sqlalchemy.ext.asyncio import AsyncSession


class BaseSessionMixin:
    def __init__(self):
        self._session: AsyncSession = session
