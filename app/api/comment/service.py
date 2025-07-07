import sys

from loguru import logger

from app.api.comment import schema
from app.exceptions.custom_exception import CustomException
from app.models.models import Comment
from app.security import TokenPayload


async def add_comment(session, current_user: TokenPayload, request: schema.StoreCommentReq):
    try:
        async with session as session:
            new_comment = Comment(
                user_id=int(current_user.sub),
                scrap_id=request.scrap_id,
                content=request.comment
            )

            session.add(new_comment)

            await session.commit()

    except CustomException as ce:
        await session.rollback()
        raise ce
    except Exception as e:
        await session.rollback()
        logger.error("error : {}", sys.exc_info())
        raise CustomException(status_code=500, message="댓글 등록 오류")
