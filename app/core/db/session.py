from asyncio import current_task
from functools import lru_cache

from core.config import get_config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


@lru_cache
def get_session() -> async_scoped_session[AsyncSession]:
    config = get_config()
    engine: AsyncEngine = create_async_engine(str(config.SQLALCHEMY_DATABASE_URI))
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    session = async_scoped_session(
        session_factory=session_factory,
        scopefunc=current_task,
    )
    return session
