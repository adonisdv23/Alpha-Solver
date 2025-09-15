from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.webapp.routes import auth, requests as request_routes, settings  # noqa: E402


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("ALPHA_DASHBOARD_PASSWORD", "testing-secret")
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRET_KEY", "unit-test-secret")
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRETS_PATH", str(tmp_path / "secrets.json"))
    monkeypatch.setenv("ALPHA_DASHBOARD_AUDIT_LOG", str(tmp_path / "audit.log"))

    auth.reset_state()
    request_routes.reset_state()

    app = FastAPI()
    auth.install_dashboard_security(app)
    app.include_router(auth.router)
    app.include_router(request_routes.router)
    app.include_router(settings.router)

    client = TestClient(app, base_url="https://testserver")
    try:
        yield client
    finally:
        client.close()


def _login(client: TestClient) -> str:
    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert response.status_code == 303
    csrf_token = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert csrf_token
    return csrf_token


def test_login_sets_secure_cookie_and_allows_access(client: TestClient) -> None:
    gate = client.get("/requests", follow_redirects=False)
    assert gate.status_code == 303
    assert gate.headers["location"] == "/login"

    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert response.status_code == 303

    session_cookie = client.cookies.get(auth.SESSION_COOKIE_NAME)
    csrf_cookie = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert session_cookie
    assert csrf_cookie

    header_value = response.headers.get("set-cookie", "").lower()
    assert auth.SESSION_COOKIE_NAME in header_value
    assert "httponly" in header_value
    assert "secure" in header_value
    assert "samesite=strict" in header_value

    page = client.get("/requests")
    assert page.status_code == 200
    assert "<form" in page.text


def test_failed_logins_trigger_lockout(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(auth, "LOCKOUT_DURATION_SECONDS", 0.5)

    for _ in range(5):
        response = client.post("/login", data={"password": "wrong"}, follow_redirects=False)
        assert response.status_code == 401

    locked = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert locked.status_code == 429
    assert "Try again later" in locked.text

    time.sleep(0.55)

    recovery = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert recovery.status_code == 303


def test_csrf_required_for_dashboard_posts(client: TestClient) -> None:
    csrf_token = _login(client)

    missing = client.post(
        "/requests",
        json={"prompt": "hello", "provider": request_routes.AVAILABLE_PROVIDERS[0]},
    )
    assert missing.status_code == 403
    assert missing.json()["detail"] == "missing CSRF token"

    valid = client.post(
        "/requests",
        json={"prompt": "hello", "provider": request_routes.AVAILABLE_PROVIDERS[0]},
        headers={"x-alpha-csrf": csrf_token},
    )
    assert valid.status_code == 200
    assert "id" in valid.json()

    settings_blocked = client.post(
        "/settings/keys",
        data={"provider": "openai", "key": "sk-test"},
        follow_redirects=False,
    )
    assert settings_blocked.status_code == 403

    settings_allowed = client.post(
        "/settings/keys",
        data={"provider": "openai", "key": "sk-test"},
        headers={"x-alpha-csrf": csrf_token},
        follow_redirects=False,
    )
    assert settings_allowed.status_code == 303


def test_logout_revokes_session(client: TestClient) -> None:
    _login(client)

    page = client.get("/requests")
    assert page.status_code == 200

    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"

    gated = client.get("/requests", follow_redirects=False)
    assert gated.status_code == 303
    assert gated.headers["location"] == "/login"


def test_password_not_logged(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level("INFO")
    _login(client)
    for record in caplog.records:
        assert "testing-secret" not in record.getMessage()
