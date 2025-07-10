import uuid

from app.api.category.schema import CreateCategoryRequest, UpdateCategoryRequest, DeleteCategoryRequest, CategoryResponse
from fastapi import status, Depends, APIRouter
from app.db.session import get_session
from app.api.common_schema import CommonRes
from app.api.category import service
from app.security import get_current_user

router = APIRouter(prefix="/category", tags=["category"])


@router.post("/", response_model=CommonRes[CategoryResponse], status_code=status.HTTP_202_ACCEPTED)
async def create_category(request: CreateCategoryRequest, current_user=Depends(get_current_user), session = Depends(get_session)):  

    category = await service.create_category(session, int(current_user.sub), request)
    
    return CommonRes(data=category)

@router.patch("/{category_id}", response_model=CommonRes[CategoryResponse])
async def update_category(category_id: int, request: UpdateCategoryRequest, current_user=Depends(get_current_user),  session = Depends(get_session)):

    category = await service.update_category(session, category_id, int(current_user.sub), request)

    return CommonRes(data=category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, current_user=Depends(get_current_user), session = Depends(get_session)):

    category = await service.delete_category(session=session, category_id=category_id, user_id=int(current_user.sub))

    return CommonRes(data=None)