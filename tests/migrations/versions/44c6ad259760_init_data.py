"""init_data

Revision ID: 44c6ad259760
Revises: 84a8feaefb90
Create Date: 2025-06-19 19:48:33.302004

"""
from typing import Sequence, Union

from alembic.op import bulk_insert

from app.models import models

# revision identifiers, used by Alembic.
revision: str = '44c6ad259760'
down_revision: Union[str, None] = '84a8feaefb90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bulk_insert(
        models.User.__table__,
        [
            {
                "provider": None,
                "login_id": "test-id1",
                "password": "password",
                "email": "test-email@test.com",
                "name": "테스트회원"
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
