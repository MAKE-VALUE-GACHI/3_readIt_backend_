import uuid

from app.api.scrap.schema import ScrapResponse, ScrapRequest, StatusResponse
from fastapi import status, Depends, APIRouter
from app.api.scrap.service import create_scrap, get_summary
from app.db.session import get_session

router = APIRouter(prefix="/scrap", tags=["scrap"])

@router.post("/summaries", response_model=ScrapResponse, status_code=status.HTTP_202_ACCEPTED)
async def request_scrap(request: ScrapRequest, session = Depends(get_session)):
    task_id = str(uuid.uuid4())    

    await create_scrap(session, task_id, request)
    
    return {"task_id": task_id}

@router.get("/summaries/{task_id}", response_model=StatusResponse)
async def get_summary_status(task_id: str, session = Depends(get_session)):

    task_data = await get_summary(session, task_id)
    
    return task_data
