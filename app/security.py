from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

import jwt
from fastapi import status, Request
from pydantic import BaseModel

from app.config import settings
from app.exceptions.CustomException import CustomException


class TokenPayload(BaseModel):
    sub: int
    email: str
    exp: int
    iat: int


class JwtTokenProvider:
    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, subject,
                     expires_delta: timedelta,
                     additional_claims: Optional[Dict[str, Any]] = None) -> str:
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        payload = {
            "sub": str(subject),
            "exp": int((now + expires_delta).timestamp()),
            "iat": int(now.timestamp()),
        }
        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_access_token(self, subject,
                            expires_delta: timedelta = timedelta(minutes=30),
                            additional_claims: Optional[Dict[str, Any]] = None) -> str:
        return self.create_token(subject, expires_delta, additional_claims)

    def create_refresh_token(self, subject,
                             expires_delta: timedelta = timedelta(days=7),
                             additional_claims: Optional[Dict[str, Any]] = None) -> str:
        return self.create_token(subject, expires_delta, additional_claims)

    def decode_token(self, token: str) -> TokenPayload:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return TokenPayload(**payload)


jwt_provider = JwtTokenProvider()


def get_jwt_provider():
    return jwt_provider


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                              message="Authorization header missing or invalid")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt_provider.decode_token(token)

        return payload
    except jwt.ExpiredSignatureError:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, message="Token expired")
    except Exception:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid token")
