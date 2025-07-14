from sqlalchemy.ext.asyncio import AsyncSession
from app.api.category.schema import CreateCategoryRequest, CategoryResponse, UpdateCategoryRequest
from sqlalchemy import select, func
from app.models.models import Category, Scrap

async def get_category_by_id(
    session: AsyncSession,
    category_id: int,
    user_id: int
) -> CategoryResponse | None:
    
    query = select(Category).where(Category.id == category_id, Category.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def get_categories_by_user_id(
    session: AsyncSession,
    user_id: int
) -> list[CategoryResponse]:

    query = select(Category).where(Category.user_id == user_id)
    result = await session.execute(query)
    categories = result.scalars().all()
    
    return [CategoryResponse.model_validate(category) for category in categories] if categories else []

async def create_category(session: AsyncSession, user_id: int, request: CreateCategoryRequest):

    category = Category(
        name=request.name,
        user_id=user_id
    )
    
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    return category

async def update_category(session: AsyncSession, db_category: Category, request: UpdateCategoryRequest):
    db_category.name = request.name
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    
    return db_category
    
async def delete_category(session: AsyncSession, db_category: Category):


    if not db_category:
        return
    
    await session.delete(db_category)
    await session.commit()
    
    return db_category

async def get_category_by_name(
    session: AsyncSession,
    *,
    user_id: int,
    name: str
):

    query = select(Category).where(
        Category.user_id == user_id,
        Category.name == name
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def count_scraps_in_category(session: AsyncSession, *, category_id: int) -> int:
    query = select(func.count(Scrap.id)).where(Scrap.category_id == category_id)
    result = await session.execute(query)
    return result.scalar_one()