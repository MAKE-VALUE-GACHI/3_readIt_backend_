from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GetUserRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    username: str = Field(validation_alias="name")


class StoreUserReq(BaseModel):
    provider: Optional[str] = None
    login_id: str
    email: str
    password: Optional[str] = None
    name: str
