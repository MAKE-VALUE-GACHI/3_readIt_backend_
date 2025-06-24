from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from loguru import logger

from app.api.user import service, schema
from app.client.oauth_client import get_oauth_client, OAuthClient
from app.db.session import get_session
from app.api.auth.schema import LoginRes
import jwt
from datetime import datetime, timedelta
from app.config import settings
from app.api.auth import service as auth_service
from app.api.auth.utils import get_jwt_provider, JwtTokenProvider

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/{provider}")
async def social_login(oauth_client: OAuthClient = Depends(get_oauth_client)):
    authorization_url = oauth_client.get_authorization_url()
    logger.debug("social_login * {}", authorization_url)

    return RedirectResponse(url=authorization_url)


@router.get(
    path="/callback/{provider}",
    name="google oauth callback",
)
async def social_callback(code: str,
                          session=Depends(get_session),
                          oauth_client: OAuthClient = Depends(get_oauth_client),
                          jwt_provider: JwtTokenProvider = Depends(get_jwt_provider)):
    access_token = oauth_client.get_access_token(code)
    user_info = oauth_client.get_user_info(access_token)
    logger.debug("social_callback * {}", user_info.model_dump())

    user = await service.get_user_by_email(session=session, email=user_info.email)

    if not user:
        store_request = schema.StoreUserReq(
            provider=oauth_client.provider,
            login_id=user_info.email,
            email=user_info.email,
            name=user_info.name,
        )
        user = await service.store_user(session, store_request)

    # JWT 토큰 생성 (JwtTokenProvider 유틸 사용)
    server_access_token = jwt_provider.create_access_token(user_info.email)
    server_refresh_token = jwt_provider.create_refresh_token(user_info.email)
    return LoginRes(access_token=server_access_token, refresh_token=server_refresh_token)
