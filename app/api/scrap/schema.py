from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StatusEnum(str, Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"

class ScrapRequest(BaseModel):
    user_id: int
    category_id: str
    type: str
    is_public: bool
    origin_url: str


class ScrapResponse(BaseModel):
    task_id: str

class StatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: StatusEnum
    user_id: int
    category_id: str
    origin_url: str
    type: str
    subject: str
    content: str
    is_public: bool
    view_count: int
    created_at: datetime
    modified_at: datetime