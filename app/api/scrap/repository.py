from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Scrap 
from app.api.scrap.schema import ScrapRequest, StatusEnum, UpdateScrapRequest
from datetime import datetime, timezone

async def create_scrap_record(
    session: AsyncSession,
    *,
    task_id: str,
    scrap_in: ScrapRequest,
    status: StatusEnum = StatusEnum.processing
) -> Scrap:

    db_scrap = Scrap(
        task_id=task_id,
        status=status,
        user_id=scrap_in.user_id,
        category_id="시사",
        type=scrap_in.type,
        subject="제목을 생성 중입니다...",
        content="",
        is_public=scrap_in.is_public,
        origin_url=str(scrap_in.origin_url)
    )
    session.add(db_scrap)
    await session.commit()
    await session.refresh(db_scrap)
    return db_scrap


async def get_scrap_by_task_id(session: AsyncSession, task_id: str) -> Scrap | None:

    query = select(Scrap).where(Scrap.task_id == task_id)
    result = await session.execute(query)
    return result.scalar()

async def get_scrap_by_id(session: AsyncSession, scrap_id: int) -> Scrap | None:

    query = select(Scrap).where(Scrap.id == scrap_id)
    result = await session.execute(query)
    return result.scalar()


async def update_scrap_with_summary(
    session: AsyncSession,
    *,
    task_id: str,
    status: StatusEnum,
    summary_data: dict
) -> Scrap | None:

    values_to_update = {
        "status": status,
        "subject": summary_data.get("subject"),
        "content": summary_data.get("content"),
        "category_id": summary_data.get("category_id")
    }
    
    query = (
        update(Scrap)
        .where(Scrap.task_id == task_id)
        .values(**values_to_update)
        .returning(Scrap)
    )
    
    result = await session.execute(query)
    await session.commit()
    return result.scalar_one_or_none()

async def update_scrap_record(session: AsyncSession, scrap, scrap_in: UpdateScrapRequest):
    
    if scrap is None:
        return None
    
    update_data = scrap_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(scrap, field, value)

    scrap.modified_at = datetime.now(timezone.utc)
    
    session.add(scrap)
    await session.commit()
    
    await session.refresh(scrap)
    
    return scrap

async def delete_scrap_record(session: AsyncSession, scrap_id: int):

    scrap_to_delete = await get_scrap_by_id(session=session, scrap_id=scrap_id)
    
    if scrap_to_delete is None:
        return None
        
    await session.delete(scrap_to_delete)
    await session.commit()
    
    return scrap_to_delete