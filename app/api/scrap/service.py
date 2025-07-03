import sys
import uuid
from app.api.scrap import schema
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependency.celery_service import celery_app
from app.api.scrap.schema import ScrapRequest, UpdateScrapRequest
from app.api.scrap.repository import create_scrap_record, get_scrap_by_task_id, update_scrap_record, get_scrap_by_id, delete_scrap_record
from app.exceptions.custom_exception import CustomException
from loguru import logger

async def create_scrap_service(session, task_id: uuid.uuid4, scrap_in: ScrapRequest) -> str:
    try:
        await create_scrap_record(
            session=session,
            task_id=task_id, 
            scrap_in=scrap_in
        )

        celery_app.send_task('app.dependency.celery_service.create_scrap_task', args=[task_id, scrap_in.origin_url, scrap_in.type])
        return schema.ScrapResponse.model_validate({"task_id":task_id})

    except Exception as e:
        logger.error("error : {}", sys.exc_info())
        raise CustomException("스크랩 생성 실패")   
    

async def get_summary(session, task_id: str):
    try:
        scrap = await get_scrap_by_task_id(session, task_id=task_id)
        if scrap is None:
            raise CustomException("스크랩 미존재")

        return schema.StatusResponse.model_validate(scrap)
    except Exception as e:
        if isinstance(e, CustomException):
            raise e
        
        logger.error("error : {}", sys.exc_info())

        raise CustomException("스크랩 조회 실패") from e


async def update_scrap_service(
    session: AsyncSession,
    scrap_id: int,
    scrap_in: UpdateScrapRequest
):
    try:
        scrap = await get_scrap_by_id(session, scrap_id=scrap_id)
        
        if scrap in None:
            raise CustomException("스크랩 미존재")
        
        scrap = await update_scrap_record(session, scrap=scrap, scrap_in=scrap_in)
        if scrap is None:
            raise CustomException("스크랩 업데이트 실패")
        
        return schema.StatusResponse.model_validate(scrap)
    except Exception as e:
        if isinstance(e, CustomException):
            raise e
        
        logger.error("error : {}", sys.exc_info())
        raise CustomException("스크랩 업데이트 실패") from e

async def delete_scrap_service(
        session: AsyncSession,
        scrap_id: int
):
    try:
        deleted_scrap = await delete_scrap_record(session=session, scrap_id=scrap_id)
        if deleted_scrap is None:
            raise CustomException("스크랩 미존재")
        
        return deleted_scrap
    except Exception as e:
        if isinstance(e, CustomException):
            raise e
        
        logger.error("error : {}", sys.exc_info())
        raise CustomException("스크랩 삭제 실패") from e