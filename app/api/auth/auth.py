from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.client.oauth_client import get_oauth_client, OAuthClient


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login/{provider}")
def social_login(oauth_client: OAuthClient = Depends(get_oauth_client)):
    authorization_url = oauth_client.get_authorization_url()
    return RedirectResponse(url=authorization_url)


@router.get("/callback/{provider}")
def social_callback(code: str, oauth_client: OAuthClient = Depends(get_oauth_client)):
    access_token = oauth_client.get_access_token(code)
    user_info = oauth_client.get_user_info(access_token)
    return user_info

