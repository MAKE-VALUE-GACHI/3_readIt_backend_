from fastapi import APIRouter, Depends
from loguru import logger

from app.api.user import schema, service
from app.db.session import get_session

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="/{user_id}",
    response_model=schema.GetUserRes
)
async def get_user(user_id: int, session=Depends(get_session)):
    logger.info("get_user * {}", user_id)

    user = await service.get_user(session, user_id)
    return user
