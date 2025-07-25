from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.api.common_schema import PagingRequest


class GetUserRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    profile_url: Optional[str] = None
    username: str = Field(validation_alias="name")


class StoreUserReq(BaseModel):
    provider: Optional[str] = None
    login_id: str
    email: str
    password: Optional[str] = None
    name: str
    picture: Optional[str] = None


class UpdateUserReq(BaseModel):
    name: str


class GetUserScrapReq(PagingRequest):
    category: Optional[str] = None


class GetUserScrapRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    subject: str
    category: str = Field(validation_alias=".", default="etc")
    created_at: datetime


class SetScrapVisibilityReq(BaseModel):
    scrap_id: int
    is_public: bool
