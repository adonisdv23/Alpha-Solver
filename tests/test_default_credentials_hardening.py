from pathlib import Path

from alpha.core.config import APISettings, ServiceAuthConfig
from alpha.webapp.routes import auth
from service.security import validate_api_key
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient


def test_service_auth_has_no_builtin_api_key_default(monkeypatch):
    monkeypatch.delenv("SERVICE_AUTH_KEYS", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)

    config = ServiceAuthConfig()

    assert config.enabled is True
    assert config.keys == []


def test_service_auth_uses_only_explicit_synthetic_test_keys(monkeypatch):
    monkeypatch.setenv("SERVICE_AUTH_KEYS", "synthetic-one, synthetic-two")
    monkeypatch.delenv("API_KEY", raising=False)

    config = ServiceAuthConfig()

    assert config.keys == ["synthetic-one", "synthetic-two"]


def test_protected_api_fails_closed_without_configured_keys(monkeypatch):
    monkeypatch.delenv("SERVICE_AUTH_KEYS", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)
    config = APISettings()

    app = FastAPI()

    @app.get("/protected")
    async def protected(request: Request):
        return {"key": validate_api_key(request, config)}

    client = TestClient(app)

    assert client.get("/protected").status_code == 401
    response = client.get("/protected", headers={config.auth.header: "dev-secret"})
    assert response.status_code == 401


def test_dashboard_password_helper_treats_missing_and_default_as_unconfigured(monkeypatch):
    monkeypatch.delenv(auth.PASSWORD_ENV_VAR, raising=False)
    assert auth.is_dashboard_password_configured() is False

    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, auth.DEFAULT_DASHBOARD_PASSWORD)
    assert auth.is_dashboard_password_configured() is False

    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, "synthetic-dashboard-secret")
    assert auth.is_dashboard_password_configured() is True


def test_docker_compose_files_do_not_inject_known_default_api_key():
    for compose_path in (
        Path("infrastructure/docker-compose.yml"),
        Path("infrastructure/docker-compose.prod.yml"),
    ):
        text = compose_path.read_text(encoding="utf-8")

        assert "API_KEY=${API_KEY:-changeme}" not in text
        assert "changeme" not in text
        required_interpolation = (
            "API_KEY=${API_KEY:?set API_KEY to a non-default operator-provided value}"
        )
        assert required_interpolation in text
