from unittest.mock import MagicMock
from urllib.parse import urlparse, parse_qs

from fastapi.testclient import TestClient
from loguru import logger

from app.api.auth.controller import get_oauth_client
from app.client.schemas.oauth_user_info import GoogleUserInfo
from app.main import app
from app.security import get_jwt_provider


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
    data = response.json()['data']
    logger.debug("response: {}", data)

    assert "access_token" in data
    assert "refresh_token" in data
    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)


def test_refresh_token_should_return_new_access_token(test_client):
    # given
    jwt_provider = get_jwt_provider()
    test_email = "testuser@example.com"
    refresh_token = jwt_provider.create_refresh_token(1, additional_claims={'email': test_email})

    headers = {"Authorization": f"Bearer {refresh_token}"}

    # when
    response = test_client.get("/auth/refresh", headers=headers)

    # then
    assert response.status_code == 200
    data = response.json()['data']
    logger.debug("refresh response: {}", data)

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    new_payload = jwt_provider.decode_token(data["access_token"])
    logger.debug("refresh payload : {}", new_payload.dict())

    # 새로운 access token이 기존 refresh token과 다른지 확인
    assert data["access_token"] != refresh_token


def test_refresh_token_without_authorization_header_should_return_401(test_client):
    # given
    # Authorization 헤더 없음

    # when
    response = test_client.get("/auth/refresh")

    # then
    assert response.status_code == 401
    data = response.json()
    assert "Authorization header with Bearer token is required" in data["message"]


def test_refresh_token_with_invalid_bearer_format_should_return_401(test_client):
    # given
    headers = {"Authorization": "InvalidFormat token123"}

    # when
    response = test_client.get("/auth/refresh", headers=headers)

    # then
    assert response.status_code == 401
    data = response.json()
    assert "Authorization header with Bearer token is required" in data["message"]


def test_refresh_token_with_invalid_token_should_return_401(test_client):
    # given
    invalid_token = "invalid.refresh.token"
    headers = {"Authorization": f"Bearer {invalid_token}"}

    # when
    response = test_client.get("/auth/refresh", headers=headers)

    # then
    assert response.status_code == 401
    data = response.json()

    logger.debug("response: {}", data)
    assert "Invalid or expired refresh token" in data["message"]
