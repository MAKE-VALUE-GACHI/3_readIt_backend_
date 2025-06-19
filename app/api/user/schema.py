from pydantic import BaseModel, ConfigDict


class GetUserRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    username: str
