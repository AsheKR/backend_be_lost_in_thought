"""Create answer table

Revision ID: ebef0846d19f
Revises: 30e2378da611
Create Date: 2023-09-17 20:35:39.668350

"""
from typing import Sequence

from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = "ebef0846d19f"
down_revision: str | None = "30e2378da611"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "answer",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.UUID, unique=True, default=uuid4, nullable=False),
        sa.Column("create_datetime", sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column("delete_datetime", sa.DateTime, nullable=True),
        sa.Column("answer", sa.VARCHAR(length=3000), nullable=False),
        sa.Column("question_id", sa.Integer, sa.ForeignKey("question.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("answer")
