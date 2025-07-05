from sqlalchemy.ext.asyncio import AsyncSession
from app.api.category.schema import CreateCategoryRequest, CategoryResponse, UpdateCategoryRequest
from sqlalchemy import select
from app.models.models import Category

async def get_category_by_id(
    session: AsyncSession,
    category_id: int,
    user_id: int
) -> CategoryResponse | None:
    
    query = select(Category).where(Category.id == category_id, Category.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


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