from typing import Optional

from fastapi import APIRouter, Depends, Header
from fastapi.responses import RedirectResponse
from loguru import logger

from app.api.auth.schema import LoginRes, RefreshTokenRes
from app.api.user import service, schema
from app.client.oauth_client import get_oauth_client, OAuthClient
from app.db.session import get_session
from app.exceptions.CustomException import CustomException
from app.security import get_jwt_provider, JwtTokenProvider

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
            picture=user_info.picture
        )
        user = await service.store_user(session, store_request)

    # JWT 토큰 생성 (JwtTokenProvider 유틸 사용)
    server_access_token = jwt_provider.create_access_token(
        subject=user.id,
        additional_claims={'email': user_info.email}
    )
    server_refresh_token = jwt_provider.create_refresh_token(
        subject=user.id,
        additional_claims={'email': user_info.email}
    )

    return LoginRes(access_token=server_access_token, refresh_token=server_refresh_token)


@router.get(
    path="/refresh",
    response_model=RefreshTokenRes
)
async def refresh_token(
        authorization: Optional[str] = Header(None),
        jwt_provider: JwtTokenProvider = Depends(get_jwt_provider)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise CustomException(status_code=401, message="Authorization header with Bearer token is required")

    refresh_token = authorization.replace("Bearer ", "")

    try:
        # refresh token 검증
        payload = jwt_provider.decode_token(refresh_token)
        user_id = payload.sub

        if not user_id:
            raise CustomException(status_code=401, message="Invalid refresh token")

        logger.debug("refresh user_id : {}", user_id)

        # 새로운 access token만 발급
        new_access_token = jwt_provider.create_access_token(
            subject=user_id,
            additional_claims={'email': payload.email}
        )

        return RefreshTokenRes(access_token=new_access_token)

    except Exception as e:
        logger.error("refresh_token error * {}", str(e))
        raise CustomException(status_code=401, message="Invalid or expired refresh token")
