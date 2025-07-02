import sys

from loguru import logger

from app.api.user import schema, repository
from app.exceptions.CustomException import CustomException
from app.models.models import User
from app.security import TokenPayload


async def get_user(session, user_id: int):
    user = await repository.find_by_id(session, user_id)

    return schema.GetUserRes.model_validate(user)


async def get_user_by_email(session, email: str):
    async with session as session:
        user = await repository.find_by_email(session, email)

        return user


async def store_user(session, request: schema.StoreUserReq):
    async with session as session:
        new_user = User(
            provider=request.provider,
            login_id=request.login_id,
            profile_url=request.picture,
            email=request.email,
            password=request.password,
            name=request.name
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


async def update_user(session, current_user: TokenPayload, request: schema.UpdateUserReq):
    try:
        async with session as session:
            user = await repository.find_by_id(session, current_user.sub)

            if not user:
                raise CustomException("회원 정보 미존재")

            user.name = request.name

            await session.commit()

    except Exception as e:
        await session.rollback()

        if isinstance(e, CustomException):
            raise e

        logger.error("error : {}", sys.exc_info())

        raise CustomException("수정 실패")
