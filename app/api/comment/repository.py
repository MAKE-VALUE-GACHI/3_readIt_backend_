from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Comment


async def find_all_by_scrap_id(session: AsyncSession, scrap_id: int, offset: int, limit: int):
    query = (
        select(Comment).
        where(Comment.scrap_id == scrap_id).
        order_by(Comment.id.desc()).
        offset(offset).
        limit(limit)
    )

    result = await session.execute(query)
    return result.scalars()


async def count_by_scrap_id(session: AsyncSession, scrap_id: int):
    query = (
        select(func.count(Comment.id)).
        where(Comment.scrap_id == scrap_id)
    )

    result = await session.execute(query)
    return result.scalar()
