from typing import AsyncIterator, Optional

from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_scoped_session[AsyncSession]] = None

    def init(self, db_url: str) -> None:
        self._engine = create_async_engine(
            url=db_url,
        )
        session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )
        self._session_maker = async_scoped_session(
            session_factory=session_maker,
            scopefunc=current_task,
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


async def get_session() -> AsyncIterator[AsyncSession]:
    async with db_manager.session() as session:
        yield session


db_manager = DatabaseSessionManager()
