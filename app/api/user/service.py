from app.api.user import schema, repository


async def get_user(session, user_id: int):
    user = await repository.find_by_id(session, user_id)

    return schema.GetUserRes.model_validate(user)
