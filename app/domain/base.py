from core.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class BaseSessionMixin:
    def __init__(self, session: async_scoped_session[AsyncSession]):
        self._session: async_scoped_session[AsyncSession] = session
