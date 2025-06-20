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
        sa.Column("email", sa.String(255)),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("modified_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.TIMESTAMP),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
