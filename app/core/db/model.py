from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[UUID] = mapped_column(unique=True, default=uuid4)
    create_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    delete_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
