from fastapi import APIRouter, Depends
from loguru import logger

from app.api.comment import schema, service
from app.api.common_schema import CommonRes, PagingResponse
from app.db.session import get_session
from app.security import get_current_user

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post(
    path="",
    name="댓글 등록",
    response_model=CommonRes
)
async def add_comment(
        request: schema.StoreCommentReq,
        session=Depends(get_session),
        current_user=Depends(get_current_user)
):
    logger.info("add_comment * {}", request)

    await service.add_comment(session, current_user, request)

    return CommonRes()


@router.get(
    path="",
    name="댓글 조회",
    response_model=CommonRes[PagingResponse[schema.GetCommentsRes]]
)
async def get_comments(
        request: schema.GetCommentsReq = Depends(),
        session=Depends(get_session)
):
    logger.info("get_comments * {}", request)

    items, total = await service.get_comments(session, request)

    return CommonRes(data=PagingResponse.create(request, total, items))
