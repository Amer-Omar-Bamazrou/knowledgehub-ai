"""add user ownership to documents

Revision ID: 88b9bd90e983
Revises: 15083866fad6
Create Date: 2026-09-24 20:49:03.154461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88b9bd90e983"
down_revision: Union[str, Sequence[str], None] = "15083866fad6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the column temporarily as nullable so existing documents
    # can be assigned to a user.
    op.add_column(
        "documents",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Assign existing documents to the existing test user.
    op.execute(
        "UPDATE documents SET user_id = 1 WHERE user_id IS NULL"
    )

    # user_id is now populated, so make it required.
    op.alter_column(
        "documents",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # Create the foreign key relationship.
    op.create_foreign_key(
        "fk_documents_user_id_users",
        "documents",
        "users",
        ["user_id"],
        ["id"],
    )

    # Create an index for efficient user-based document queries.
    op.create_index(
        op.f("ix_documents_user_id"),
        "documents",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_documents_user_id"),
        table_name="documents",
    )

    op.drop_constraint(
        "fk_documents_user_id_users",
        "documents",
        type_="foreignkey",
    )

    op.drop_column(
        "documents",
        "user_id",
    )
