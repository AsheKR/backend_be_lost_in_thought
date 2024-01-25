from collections.abc import AsyncIterable

from core.db.session import SessionLocal
from sqlalchemy.orm import Session


async def get_db() -> AsyncIterable[Session]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
