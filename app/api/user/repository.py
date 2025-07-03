from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.models import User, Scrap, Category


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


async def find_all_scrap_by_user_id(session: AsyncSession, user_id: int, filter_dict: dict, offset: int, limit: int):
    query = select(Scrap).options(contains_eager(Scrap.category)).join(Scrap.category)

    conditions = [Scrap.user_id == user_id]

    if filter_dict.get('category'):
        conditions.append(Category.name == filter_dict['category'])

    query = query.where(and_(*conditions)).order_by(Scrap.id.desc()).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.scalars()


async def count_scrap_by_user_id(session: AsyncSession, user_id: int, filter_dict: dict):
    query = select(func.count(Scrap.id)).join(Scrap.category)
    
    conditions = [Scrap.user_id == user_id]

    if filter_dict.get('category'):
        conditions.append(Category.name == filter_dict['category'])

    query = query.where(and_(*conditions))
    result = await session.execute(query)
    return result.scalar()
