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
    bulk_insert(
        models.Scrap.__table__,
        [
            {
                "id": 1,
                "task_id": "task-1",
                "status": "processing",
                "user_id": 1,
                "category_id": 1,
                "type": "one-line",
                "subject": "테스트 스크랩",
                "content": "테스트 스크랩 내용",
                "is_public": True,
                "view_count": 0,
                "origin_url": "https://example.com/test-scrap",
                "created_at": "2025-06-19 19:48:33.302004",
                "modified_at": "2025-06-19 19:48:33.302004"
            },
            {
                "id": 2,
                "task_id": "task-2",
                "status": "processing",
                "user_id": 1,
                "category_id": 1,
                "type": "one-line",
                "subject": "테스트 스크랩",
                "content": "테스트 스크랩 내용",
                "is_public": False,
                "view_count": 0,
                "origin_url": "https://example.com/test-scrap",
                "created_at": "2025-06-19 19:48:33.302004",
                "modified_at": "2025-06-19 19:48:33.302004"
            }
        ]
    )
    bulk_insert(
        models.Category.__table__,
        [
            {
                "id": 1,
                "user_id": 1,
                "name": "뉴스"
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
