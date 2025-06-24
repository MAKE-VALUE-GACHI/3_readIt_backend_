from pydantic import BaseModel


class LoginRes(BaseModel):
    access_token: str
    refresh_token: str
