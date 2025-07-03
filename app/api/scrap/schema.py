from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StatusEnum(str, Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"

class ScrapRequest(BaseModel):
    user_id: int
    category_id: int
    type: str
    is_public: bool
    origin_url: str


class ScrapResponse(BaseModel):
    task_id: str

class StatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: StatusEnum
    user_id: int
    category_id: int
    origin_url: str
    type: str
    subject: str
    content: str
    is_public: bool
    view_count: int
    created_at: datetime
    modified_at: datetime

class UpdateScrapRequest(BaseModel):
    category_id: int
    type: str
    subject: str
    content: str
    is_public: bool
