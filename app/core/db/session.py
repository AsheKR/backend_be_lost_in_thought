from asyncio import current_task

from core.config import get_config
from sqlalchemy.ext.asyncio import AsyncEngine, async_scoped_session, async_sessionmaker, create_async_engine

config = get_config()
engine: AsyncEngine = create_async_engine(str(config.SQLALCHEMY_DATABASE_URI), echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
session = async_scoped_session(
    session_factory=session_factory,
    scopefunc=current_task,
)
