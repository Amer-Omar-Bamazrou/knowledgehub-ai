"""add embeddings to document chunks

Revision ID: b21e37dcdd0d
Revises: 40dee47a0037
Create Date: 2026-09-27 21:01:49.422792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "b21e37dcdd0d"
down_revision: Union[str, Sequence[str], None] = "40dee47a0037"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(768),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "document_chunks",
        "embedding",
    )