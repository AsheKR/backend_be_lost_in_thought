"""Create language table

Revision ID: f8ab1017d1df
Revises: ebef0846d19f
Create Date: 2023-09-22 18:54:24.243416

"""
from typing import Sequence

from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = "f8ab1017d1df"
down_revision: str | None = "ba852a5526d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "language",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.UUID, unique=True, default=uuid4, nullable=False),
        sa.Column("create_datetime", sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column("delete_datetime", sa.DateTime, nullable=True),
        sa.Column("code", sa.VARCHAR(length=8), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("language")
