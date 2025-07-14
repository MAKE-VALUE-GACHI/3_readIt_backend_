from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CreateCategoryRequest(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str


class UpdateCategoryRequest(BaseModel):
    name: str

class DeleteCategoryRequest(BaseModel):
    pass

class CategoryResponseList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    categories: list[CategoryResponse]