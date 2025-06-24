from pydantic import BaseModel, EmailStr

class OAuthUserInfo(BaseModel):
    id: str
    email: EmailStr
    name: str
    picture: str

class GoogleUserInfo(OAuthUserInfo):
    verified_email: bool
    given_name: str
    family_name: str
    locale: str 