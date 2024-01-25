"""Create Default User Table

Revision ID: ba852a5526d6
Revises:
Create Date: 2023-08-24 12:52:35.043755

"""
from collections.abc import Sequence
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ba852a5526d6"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.UUID, unique=True, default=uuid4),
    )


def downgrade() -> None:
    op.drop_table("user")
