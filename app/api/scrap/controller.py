import uuid

from fastapi import status, Depends, APIRouter

from app.api.common_schema import CommonRes
from app.api.scrap.schema import ScrapResponse, ScrapRequest, StatusResponse, UpdateScrapRequest, PaginatedScrapResponse
from app.api.scrap.service import create_scrap_service, get_summary, update_scrap_service, delete_scrap_service, \
    add_scrap_like, revoke_scrap_like, get_paginated_scraps
from app.db.session import get_session
from app.security import get_current_user
from app.models.enums import ScrapOrderType
from app.api.common_schema import PagingRequest

router = APIRouter(prefix="/scrap", tags=["scrap"])


@router.post("/summaries", response_model=CommonRes[ScrapResponse], status_code=status.HTTP_202_ACCEPTED)
async def request_scrap(request: ScrapRequest, current_user=Depends(get_current_user), session=Depends(get_session)):
    task_id = str(uuid.uuid4())

    await create_scrap_service(session, task_id, request, int(current_user.sub))

    return CommonRes(data={"task_id": task_id})


@router.get("/summaries/{task_id}", response_model=CommonRes[StatusResponse])
async def get_summary_status(task_id: str, session=Depends(get_session)):
    task_data = await get_summary(session, task_id)

    return CommonRes(data=task_data)


@router.patch("/{scrap_id}", response_model=CommonRes[StatusResponse])
async def update_scrap(scrap_id: int, scrap_in: UpdateScrapRequest, session=Depends(get_session), current_user=Depends(get_current_user)):
    scrap = await update_scrap_service(session, scrap_id=scrap_id, scrap_in=scrap_in, user_id=int(current_user.sub))

    return CommonRes(data=scrap)


@router.delete("/{scrap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scrap(scrap_id, session=Depends(get_session), current_user=Depends(get_current_user)):
    deleted_scrap = await delete_scrap_service(session=session, scrap_id=scrap_id, user_id=int(current_user.sub))

    return CommonRes()


@router.patch("/{scrap_id}/like", response_model=CommonRes[StatusResponse])
async def like(scrap_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    scrap = await add_scrap_like(session, current_user, scrap_id)

    return CommonRes(data=scrap)


@router.patch("/{scrap_id}/unlike", response_model=CommonRes[StatusResponse])
async def unlike(scrap_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    scrap = await revoke_scrap_like(session, current_user, scrap_id)

    return CommonRes(data=scrap)


@router.get("/likes", response_model=CommonRes[PaginatedScrapResponse])
async def get_scrap_list(
    paging: PagingRequest = Depends(),
    
    session = Depends(get_session)
):
    paginated_result = await get_paginated_scraps(
        session=session,
        order_by=ScrapOrderType.LIKE,
        paging_params=paging
    )
    return CommonRes(data=paginated_result)

@router.get("/views", response_model=CommonRes[PaginatedScrapResponse])
async def get_scrap_list(
    paging: PagingRequest = Depends(),
    session = Depends(get_session)
):
    paginated_result = await get_paginated_scraps(
        session=session,
        order_by=ScrapOrderType.VIEW,
        paging_params=paging
    )
    return CommonRes(data=paginated_result)

@router.get("/latest", response_model=CommonRes[PaginatedScrapResponse])
async def get_scrap_list(
    paging: PagingRequest = Depends(),
    session = Depends(get_session)
):
    paginated_result = await get_paginated_scraps(
        session=session,
        order_by=ScrapOrderType.LATEST,
        paging_params=paging
    )
    return CommonRes(data=paginated_result)
