from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

T = TypeVar("T")


class CommonRes(BaseModel, Generic[T]):
    status: str = "success"
    code: int = 200
    message: str = "요청 처리 성공"
    data: Optional[T] = None


class PagingRequest(BaseModel):
    page: int = 1
    size: int = 20

    def get_offset_limit(self) -> (int, int):
        if self.size < 1:
            self.size = 20

        if self.page < 1:
            self.page = 1

        offset = (self.page - 1) * self.size
        limit = self.size

        return offset, limit


class PagingResponse(BaseModel, Generic[T]):
    page: int
    size: int
    total_count: int
    total_pages: int
    content: List[T]

    @staticmethod
    def create(request: PagingRequest, total: int, content: List[T]) -> "PagingResponse[T]":
        total_page, remain = divmod(total, request.size)
        if remain > 0:
            total_page += 1

        return PagingResponse(
            page=request.page,
            size=request.size,
            total_count=total,
            total_pages=total_page,
            content=content
        )
