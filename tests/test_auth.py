from unittest.mock import MagicMock
from urllib.parse import urlparse, parse_qs

from fastapi.testclient import TestClient
from loguru import logger

from app.api.auth.controller import get_oauth_client
from app.client.schemas.oauth_user_info import GoogleUserInfo
from app.main import app


def test_google_login_should_redirect_to_google_authorization_url(test_client: TestClient):
    # given
    provider = "google"

    # when
    response = test_client.get(f"/auth/login/{provider}", follow_redirects=False)

    logger.debug("response: {}", response.headers)

    # then
    assert response.status_code == 307
    location = response.headers.get("Location")
    assert location is not None

    parsed_location = urlparse(location)
    assert parsed_location.scheme == "https"
    assert parsed_location.netloc == "accounts.google.com"
    assert parsed_location.path == "/o/oauth2/auth"

    query_params = parse_qs(parsed_location.query)
    assert "response_type" in query_params
    assert "client_id" in query_params
    assert "redirect_uri" in query_params
    assert "scope" in query_params
    assert "access_type" in query_params
    assert "include_granted_scopes" in query_params


def make_mock_oauth_client():
    mock_client = MagicMock()
    mock_client.provider = "google"
    mock_client.get_access_token.return_value = "mock_access_token"
    mock_user_info = GoogleUserInfo(
        id="1234567890",
        email="testuser@example.com",
        name="테스트유저",
        picture="http://example.com/pic.jpg",
        verified_email=True,
        given_name="테스트",
        family_name="유저",
        locale="ko"
    )
    mock_client.get_user_info.return_value = mock_user_info
    return mock_client


def test_social_callback_should_return_jwt_token(setup_database, test_client):
    # given
    mock_oauth_client = make_mock_oauth_client()
    app.dependency_overrides[get_oauth_client] = lambda: mock_oauth_client

    provider = "google"
    code = "dummy_code"

    # when
    response = test_client.get(f"/auth/callback/{provider}?code={code}")

    # then
    assert response.status_code == 200
    data = response.json()
    logger.debug("response: {}", data)

    assert "access_token" in data
    assert "refresh_token" in data
    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)
