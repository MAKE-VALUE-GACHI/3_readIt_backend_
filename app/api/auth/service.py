import jwt
from datetime import datetime, timedelta
from app.config import settings

def create_access_token(subject: str, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject,
        "exp": now + expires_delta,
        "iat": now,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(subject: str, expires_delta: timedelta = timedelta(days=7)) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject,
        "exp": now + expires_delta,
        "iat": now,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def create_token_pair(subject: str):
    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)
    return access_token, refresh_token 