import uuid

from app.api.scrap.schema import ScrapResponse, ScrapRequest, StatusResponse, UpdateScrapRequest
from fastapi import status, Depends, APIRouter, HTTPException
from app.api.scrap.service import create_scrap_service, get_summary, update_scrap_service, delete_scrap_service
from app.db.session import get_session
from app.api.common_schema import CommonRes

router = APIRouter(prefix="/scrap", tags=["scrap"])

# user id 추가필요
@router.post("/summaries", response_model=CommonRes[ScrapResponse], status_code=status.HTTP_202_ACCEPTED)
async def request_scrap(request: ScrapRequest, session = Depends(get_session)):
    task_id = str(uuid.uuid4())    

    await create_scrap_service(session, task_id, request)
    
    return CommonRes(data={"task_id": task_id})

@router.get("/summaries/{task_id}", response_model=CommonRes[StatusResponse])
async def get_summary_status(task_id: str, session = Depends(get_session)):

    task_data = await get_summary(session, task_id)
    
    return CommonRes(data=task_data)

@router.patch("/{scrap_id}", response_model=CommonRes[StatusResponse])
async def update_scrap(scrap_id: int, scrap_in: UpdateScrapRequest, session = Depends(get_session)):

    scrap = await update_scrap_service(session, scrap_id=scrap_id, scrap_in=scrap_in)

    return CommonRes(data=scrap)

@router.delete("/{scrap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scrap(scrap_id, session = Depends(get_session)):

    deleted_scrap = await delete_scrap_service(session=session, scrap_id=scrap_id)

    return