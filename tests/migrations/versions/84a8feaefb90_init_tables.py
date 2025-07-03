"""init_tables

Revision ID: 84a8feaefb90
Revises: 
Create Date: 2025-06-16 21:14:51.034179

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '84a8feaefb90'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("provider", sa.String(255)),
        sa.Column("login_id", sa.String(255), unique=True, nullable=False),
        sa.Column("password", sa.String(255)),
        sa.Column("name", sa.String(255)),
        sa.Column("profile_url", sa.String(255)),
        sa.Column("email", sa.String(255)),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("modified_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.TIMESTAMP),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "scrap",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(255), unique=True, nullable=False),
        sa.Column("status", sa.String(255), nullable=False, server_default=sa.text("'processing'")),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("category_id", sa.String(255), nullable=True),
        sa.Column("type", sa.String(255), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("content", sa.String(2000), nullable=False),
        sa.Column("is_public", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("view_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("origin_url", sa.String(255), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("modified_at", sa.TIMESTAMP(timezone=True), nullable=False)
    )
    op.create_table(
        "category",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(255), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
