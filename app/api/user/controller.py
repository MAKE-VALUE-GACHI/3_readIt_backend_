from fastapi import APIRouter, Depends
from loguru import logger

from app.api.user import schema, service
from app.db.session import get_session
from app.security import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="/{user_id}",
    response_model=schema.GetUserRes
)
async def get_user(user_id: int, session=Depends(get_session)):
    logger.info("get_user * {}", user_id)

    user = await service.get_user(session, user_id)
    return user


@router.put(
    path="",
)
async def update_user(
        request: schema.UpdateUserReq,
        session=Depends(get_session),
        current_user=Depends(get_current_user)
):
    logger.info("update_user * {}", current_user.sub)

    await service.update_user(session, current_user, request)

    return True
