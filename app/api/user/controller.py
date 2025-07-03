from fastapi import APIRouter, Depends
from loguru import logger

from app.api.common_schema import CommonRes, PagingResponse
from app.api.user import schema, service
from app.db.session import get_session
from app.security import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="",
    response_model=CommonRes[schema.GetUserRes]
)
async def get_user(current_user=Depends(get_current_user), session=Depends(get_session)):
    logger.info("get_user * {}", current_user.sub)

    user = await service.get_user(session, current_user)
    return CommonRes(data=user)


@router.put(
    path="",
    response_model=CommonRes
)
async def update_user(
        request: schema.UpdateUserReq,
        session=Depends(get_session),
        current_user=Depends(get_current_user)
):
    logger.info("update_user * {}", current_user.sub)

    await service.update_user(session, current_user, request)

    return CommonRes()


@router.get(
    path="/scraps",
    response_model=CommonRes[PagingResponse[schema.GetUserScrapRes]]
)
async def my_scraps(
        request: schema.GetUserScrapReq = Depends(),
        session=Depends(get_session),
        current_user=Depends(get_current_user)
):
    logger.info("my_scraps * {}", request)

    contents, total = await service.get_scraps(session, current_user, request)

    return CommonRes(data=PagingResponse.create(request, total, contents))
