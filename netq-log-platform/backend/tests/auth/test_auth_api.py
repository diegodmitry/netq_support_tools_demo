from fastapi.testclient import TestClient

from app.main import app


def test_auth_config_exposes_supported_domains() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/auth/config")

    assert response.status_code == 200
    body = response.json()

    assert "domains" in body
    assert any(domain["default"] for domain in body["domains"])


def test_login_creates_authenticated_session_cookie() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "jdoe",
            "password": "secret",
        },
    )

    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert "netq_session" in response.cookies


def test_login_rejects_invalid_credentials() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "jdoe",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


def test_login_rejects_unauthorized_user() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "not-allowed",
            "password": "secret",
        },
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "AUTH_FORBIDDEN"


def test_session_endpoint_returns_authenticated_user_after_login() -> None:
    client = TestClient(app)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "jdoe",
            "password": "secret",
        },
    )

    assert login_response.status_code == 200

    response = client.get("/api/v1/auth/session")

    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert response.json()["user"]["username"] == "jdoe"


def test_keep_alive_requires_authenticated_session() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/auth/keep-alive", json={})

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "SESSION_EXPIRED"


def test_keep_alive_renews_authenticated_session_cookie() -> None:
    client = TestClient(app)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "jdoe",
            "password": "secret",
        },
    )

    assert login_response.status_code == 200

    response = client.post("/api/v1/auth/keep-alive", json={})

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert "netq_session" in response.cookies


def test_logout_is_idempotent_from_user_perspective() -> None:
    client = TestClient(app)
    response = client.delete("/api/v1/auth/session")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "loggedOut": True, "redirectTo": "/login"}


def test_logout_invalidates_session_and_sets_no_cache_headers() -> None:
    client = TestClient(app)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "domain": "ptportugal",
            "username": "jdoe",
            "password": "secret",
        },
    )

    assert login_response.status_code == 200

    logout_response = client.delete("/api/v1/auth/session")

    assert logout_response.status_code == 200
    assert logout_response.headers["cache-control"] == "no-store"
    assert logout_response.headers["pragma"] == "no-cache"
    assert logout_response.headers["expires"] == "Thu, 01 Jan 1970 00:00:00 GMT"

    session_response = client.get("/api/v1/auth/session")

    assert session_response.status_code == 401
    assert session_response.json()["error"]["code"] == "SESSION_NOT_AUTHENTICATED"
