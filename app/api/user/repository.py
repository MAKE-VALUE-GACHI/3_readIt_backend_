from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.models import User, Scrap


async def find_by_id(session: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.id == user_id)

    result = await session.execute(query)
    return result.scalar()


async def find_by_email_and_provider(session: AsyncSession, email: str, provider: str) -> User:
    query = (
        select(User).
        where(User.provider == provider).
        where(User.login_id == email).
        where(User.deleted_at.is_(None))
    )

    result = await session.execute(query)
    return result.scalar()


async def find_all_scrap_by_user_id(session: AsyncSession, user_id: int, offset: int, limit: int):
    query = (
        select(Scrap).
        options(contains_eager(Scrap.category)).
        where(Scrap.user_id == user_id).
        order_by(Scrap.id.desc()).
        offset(offset).
        limit(limit)
    )

    result = await session.execute(query)
    return result.scalars()


async def count_scrap_by_user_id(session: AsyncSession, user_id: int):
    from sqlalchemy import func
    query = (
        select(func.count(Scrap.id)).
        where(Scrap.user_id == user_id)
    )

    result = await session.execute(query)
    return result.scalar()
