from fastapi.testclient import TestClient
from urllib.parse import urlparse, parse_qs


def test_google_login_should_redirect_to_google_authorization_url(test_client: TestClient):
    # given
    provider = "google"

    # when
    response = test_client.get(f"/api/auth/login/{provider}", follow_redirects=False)

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
