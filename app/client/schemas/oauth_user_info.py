from typing import Optional

from pydantic import BaseModel


class OAuthUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: str


class GoogleUserInfo(OAuthUserInfo):
    verified_email: bool
    given_name: str
    family_name: str
    locale: Optional[str] = None
