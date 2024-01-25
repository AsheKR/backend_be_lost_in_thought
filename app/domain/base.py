from core.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class BaseSessionMixin:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
