from app.api.user import schema, repository
from app.models.models import User


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
            email=request.email,
            password=request.password,
            name=request.name
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
