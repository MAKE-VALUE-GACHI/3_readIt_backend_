from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import List, Optional
from app.models.enums import ScrapType


class StatusEnum(str, Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ScrapRequest(BaseModel):
    category_id: Optional[int]
    type: ScrapType
    is_public: bool
    origin_url: Optional[HttpUrl] = None
    text: Optional[str] = None


class CreateScrapResponse(BaseModel):
    task_id: str


class StatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: StatusEnum
    user_id: int
    category_id: Optional[int]
    origin_url: Optional[HttpUrl] = None
    text: Optional[str] = None
    type: str
    subject: str
    content: str
    is_public: bool
    like_count: int
    view_count: int
    created_at: datetime
    modified_at: datetime


class UpdateScrapRequest(BaseModel):
    category_id: Optional[int] = None
    type: str
    subject: str
    content: str
    is_public: bool


class ScrapResponse(BaseModel):
    id: int
    subject: str
    content: str | None = None
    like_count: int
    view_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- 목록 조회를 위한 페이지네이션 응답 ---
class PaginatedScrapResponse(BaseModel):
    total: int # 전체 아이템 개수
    items: List[ScrapResponse] # 현재 페이지의 아이템 목록