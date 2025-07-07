from pydantic import BaseModel


class StoreCommentReq(BaseModel):
    scrap_id: int
    comment: str
