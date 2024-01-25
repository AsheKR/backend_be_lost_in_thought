from core.db.session import session
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class BaseSessionMixin:
    def __init__(self):
        self._session: async_scoped_session[AsyncSession] = session
