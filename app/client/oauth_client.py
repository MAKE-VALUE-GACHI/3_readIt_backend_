from abc import ABC, abstractmethod
from app.config import settings
import httpx
from app.client.schemas.oauth_user_info import OAuthUserInfo, GoogleUserInfo

class OAuthClient(ABC):

    @abstractmethod
    def get_authorization_url(self) -> str:
        pass

    @abstractmethod
    def get_access_token(self, code: str) -> str:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> OAuthUserInfo:
        pass
    


class GoogleOAuthClient(OAuthClient):
    """
    Google OAuth Client
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self) -> str:
        base_url = "https://accounts.google.com/o/oauth2/auth"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            "access_type": "offline",
            "include_granted_scopes": "true",
        }
        return str(httpx.URL(base_url, params=params))

    def get_access_token(self, code: str) -> str:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response = httpx.post(token_url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_user_info(self, access_token: str) -> OAuthUserInfo:
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = httpx.get(user_info_url, headers=headers)
        response.raise_for_status()
        return GoogleUserInfo(**response.json())


def get_oauth_client(provider: str) -> OAuthClient:
    if provider == "google":
        return GoogleOAuthClient(
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            settings.GOOGLE_REDIRECT_URI,
        )
    else:
        raise ValueError(f"Invalid provider: {provider}")
