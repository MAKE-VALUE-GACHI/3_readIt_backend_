import sys

from loguru import logger

from app.api.user import schema, repository
from app.exceptions.custom_exception import CustomException
from app.models.models import User
from app.security import TokenPayload


async def get_user(session, current_user: TokenPayload):
    user = await repository.find_by_id(session, int(current_user.sub))

    return schema.GetUserRes.model_validate(user)


async def get_user_by_email_and_provider(session, email: str, provider: str):
    async with session as session:
        user = await repository.find_by_email_and_provider(session, email, provider)

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
            user = await repository.find_by_id(session, int(current_user.sub))

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


async def get_scraps(session, current_user: TokenPayload, request: schema.GetUserScrapReq):
    async with session as session:
        try:
            offset, limit = request.get_offset_limit()
            filter_dict = {"category": request.category}

            scraps = await repository.find_all_scrap_by_user_id(
                session,
                int(current_user.sub),
                filter_dict,
                offset,
                limit
            )
            total = await repository.count_scrap_by_user_id(session, int(current_user.sub), filter_dict)

            contents = []
            for scrap in scraps:
                item = schema.GetUserScrapRes.model_validate(scrap)
                item.category_name = scrap.category.name if scrap.category else "etc"
                contents.append(item)

            return contents, total
        except CustomException as ce:
            await session.rollback()
            raise ce
        except Exception as e:
            await session.rollback()
            logger.error("error : {}", sys.exc_info())
            raise CustomException("스크랩 조회 실패")
