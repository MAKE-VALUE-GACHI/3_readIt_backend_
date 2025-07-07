from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.api.common_schema import PagingRequest


class StoreCommentReq(BaseModel):
    scrap_id: int
    comment: str


class GetCommentsReq(PagingRequest):
    scrap_id: int


class GetCommentsRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime
