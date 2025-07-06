from sqlalchemy.ext.asyncio import AsyncSession
from app.api.category.schema import CreateCategoryRequest, CategoryResponse, UpdateCategoryRequest
from app.api.category import repository
from app.exceptions.custom_exception import CustomException

from loguru import logger
import sys

async def create_category(session: AsyncSession, user_id: int, request: CreateCategoryRequest) -> CategoryResponse:

    category = await repository.create_category(session, user_id, request)
    return CategoryResponse.model_validate(category)

async def update_category(session: AsyncSession, category_id: int, user_id: int, request: UpdateCategoryRequest):
    try:
        async with session as session:
            db_category = await repository.get_category_by_id(session, category_id, user_id)
            
            if not db_category:
                raise CustomException("존재하지 않는 카테고리")
            
            updated_category = await repository.update_category(session, db_category, request)
            return CategoryResponse.model_validate(updated_category)
    
    except Exception as e:
        await session.rollback()

        if isinstance(e, CustomException):
            raise e
        
        logger.error("error : {}", sys.exc_info())

        raise CustomException("카테고리 수정 실패")

async def delete_category(session: AsyncSession, category_id: int, user_id: int):
    try:
        async with session as session:
            db_category = await repository.get_category_by_id(session, category_id, user_id)
            
            if not db_category:
                raise CustomException("존재하지 않는 카테고리")
            
            await repository.delete_category(session, db_category)
            return db_category
    except Exception as e:
        await session.rollback()
        
        if isinstance(e, CustomException):
            raise e
        
        logger.error("error : {}", sys.exc_info())

        raise CustomException("카테고리 삭제 실패")