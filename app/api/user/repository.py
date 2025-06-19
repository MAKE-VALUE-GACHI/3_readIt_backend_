from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


async def find_by_id(session: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)

    result = await session.execute(query)
    return result.scalar()
