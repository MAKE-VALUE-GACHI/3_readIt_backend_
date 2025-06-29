from celery import Celery
from app.api.scrap.schema import StatusEnum
from app.db.session import AsyncSessionLocal
import asyncio

from sqlalchemy import select
from app.models.models import Scrap

celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@celery_app.task
def create_scrap_task(task_id: str, url: str):


    async def _async_update_db():

        async with AsyncSessionLocal() as session:
            try:
                print(f"[{task_id}] AI 요약 중...")
                await asyncio.sleep(10)
                summary_data = {
                    "subject": f"'{url}'의 요약 제목",
                    "content": "AI가 생성한 요약 내용입니다...",
                }
                status = StatusEnum.completed.value
            except Exception as e:
                summary_data = {}
                status = StatusEnum.failed.value

            
            result = await session.execute(
                select(Scrap).where(Scrap.task_id == task_id)
            )
            scrap = result.scalar_one_or_none()
            if scrap:
                scrap.status = status
                scrap.subject = summary_data.get("subject", "")
                scrap.content = summary_data.get("content", "")
                await session.commit()
            else:
                pass

    try:
        asyncio.run(_async_update_db())
    except Exception as e:
        pass