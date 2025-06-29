import jwt
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from app.config import settings

class JwtTokenProvider:
    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, subject: str, expires_delta: timedelta, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        now = datetime.utcnow()
        payload = {
            "sub": subject,
            "exp": now + expires_delta,
            "iat": now,
        }
        if additional_claims:
            payload.update(additional_claims)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_access_token(self, subject: str, expires_delta: timedelta = timedelta(minutes=30), additional_claims: Optional[Dict[str, Any]] = None) -> str:
        return self.create_token(subject, expires_delta, additional_claims)

    def create_refresh_token(self, subject: str, expires_delta: timedelta = timedelta(days=7), additional_claims: Optional[Dict[str, Any]] = None) -> str:
        return self.create_token(subject, expires_delta, additional_claims)

    def decode_token(self, token: str) -> Dict[str, Any]:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

jwt_provider = JwtTokenProvider()

def get_jwt_provider():
    return jwt_provider 