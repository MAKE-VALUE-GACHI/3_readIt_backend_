import sys
import uuid

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.scrap import schema
from app.api.scrap.repository import create_scrap_record, get_scrap_by_task_id, update_scrap_record, get_scrap_by_id, \
    delete_scrap_record, get_scrap_like_by_ids, get_scraps_with_ordering
from app.api.scrap.schema import ScrapRequest, UpdateScrapRequest, PaginatedScrapResponse
from app.dependency.celery_service import celery_app
from app.exceptions.custom_exception import CustomException
from app.models.models import ScrapLike
from app.security import TokenPayload
from app.api.common_schema import PagingRequest
from app.api.category.repository import get_category_by_name


async def create_scrap_service(session, task_id: uuid.uuid4, scrap_in: ScrapRequest, user_id) -> str:
    try:
        category_id = scrap_in.category_id

        if category_id is None:
            default_category = await get_category_by_name(session, user_id=user_id, name="기타")
        
            if not default_category:
                raise CustomException("기본 카테고리 미존재")
            
            category_id = default_category.id

        scrap = await create_scrap_record(
            session=session,
            task_id=task_id,
            scrap_in=scrap_in,
            user_id=user_id
        )
        if not scrap:
            raise CustomException("스크랩 생성 실패")

        celery_app.send_task('app.dependency.celery_service.create_scrap_task',
                             args=[task_id, scrap_in.origin_url, scrap_in.type])
        return schema.CreateScrapResponse.model_validate({"task_id": task_id})

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
        scrap_in: UpdateScrapRequest,
        user_id: int
):
    try:
        scrap = await get_scrap_by_id(session, scrap_id=scrap_id, user_id=user_id)

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
        scrap_id: int,
        user_id: int
):
    try:
        deleted_scrap = await delete_scrap_record(session=session, scrap_id=scrap_id, user_id=user_id)
        if deleted_scrap is None:
            raise CustomException("스크랩 미존재")

        return deleted_scrap
    except Exception as e:
        if isinstance(e, CustomException):
            raise e

        logger.error("error : {}", sys.exc_info())
        raise CustomException("스크랩 삭제 실패") from e


async def add_scrap_like(session: AsyncSession, current_user: TokenPayload, scrap_id: int):
    try:
        async with session as session:
            scrap = await get_scrap_by_id(session, scrap_id)

            if not scrap:
                raise CustomException(status_code=404, message="스크랩 정보 미존재")

            new_like = ScrapLike(
                scrap_id=scrap_id,
                user_id=int(current_user.sub)
            )
            session.add(new_like)

            scrap.like_count += 1

            await session.commit()

            return schema.StatusResponse.model_validate(scrap)

    except Exception as e:
        await session.rollback()

        if isinstance(e, CustomException):
            raise e

        logger.error("error : {}", sys.exc_info())
        raise CustomException(status_code=500, message="스크랩 공감 오류") from e


async def revoke_scrap_like(session: AsyncSession, current_user: TokenPayload, scrap_id: int):
    try:
        async with session as session:
            scrap = await get_scrap_by_id(session, scrap_id)

            if not scrap:
                raise CustomException(status_code=404, message="스크랩 정보 미존재")

            scrap_like = await get_scrap_like_by_ids(session, scrap_id, int(current_user.sub))

            if not scrap_like:
                raise CustomException(status_code=400, message="공감 정보 미존재")

            await session.delete(scrap_like)

            if 0 < scrap.like_count:
                scrap.like_count -= 1

            await session.commit()

            return schema.StatusResponse.model_validate(scrap)

    except Exception as e:
        await session.rollback()

        if isinstance(e, CustomException):
            raise e

        logger.error("error : {}", sys.exc_info())
        raise CustomException(status_code=500, message="스크랩 공감 오류") from e


async def get_paginated_scraps(
    session: AsyncSession,
    *,
    order_by: str,
    paging_params: PagingRequest
):

    skip, limit = paging_params.get_offset_limit()
    
    total, scraps = await get_scraps_with_ordering(
        session=session,
        order_by=order_by,
        skip=skip,
        limit=limit
    )
    
    return PaginatedScrapResponse(total=total, items=scraps)