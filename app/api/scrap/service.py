import uuid
from app.api.scrap import schema
from app.dependency.celery_service import celery_app
from app.api.scrap.schema import ScrapRequest
from app.api.scrap.repository import create_scrap_record, get_scrap_by_task_id

async def create_scrap(session, task_id: uuid.uuid4, scrap_in: ScrapRequest) -> str:
    
    await create_scrap_record(
        session=session,
        task_id=task_id, 
        scrap_in=scrap_in
    )

    celery_app.send_task('app.dependency.celery_service.create_scrap_task', args=[task_id, scrap_in.origin_url])
    
    return schema.ScrapResponse.model_validate({"task_id":task_id})

async def get_summary(session, task_id: str):
    scrap = await get_scrap_by_task_id(session, task_id=task_id)

    return schema.StatusResponse.model_validate(scrap)