import pytest
from fastapi.testclient import TestClient
from starlette.middleware import Middleware

from alpha.core.config import APISettings, DEFAULT_LOCAL_CORS_ORIGINS, ServiceCorsConfig
from service.app import app


def test_service_cors_defaults_are_local_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SERVICE_CORS_ORIGINS", raising=False)
    monkeypatch.delenv("SERVICE_CORS_ALLOW_CREDENTIALS", raising=False)

    cfg = APISettings()

    assert cfg.cors.origins == DEFAULT_LOCAL_CORS_ORIGINS
    assert cfg.cors.allow_credentials is True
    assert "*" not in cfg.cors.origins
    assert cfg.cors.external_origins == []


def test_service_cors_explicit_allowlist_allows_external_origin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "SERVICE_CORS_ORIGINS",
        "https://dashboard.example.com, http://localhost:3000",
    )
    monkeypatch.delenv("SERVICE_CORS_ALLOW_CREDENTIALS", raising=False)

    cfg = APISettings()

    assert cfg.cors.origins == ["https://dashboard.example.com", "http://localhost:3000"]
    assert cfg.cors.allow_credentials is True
    assert cfg.cors.external_origins == ["https://dashboard.example.com"]


def test_service_cors_allow_credentials_reads_env_per_instance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SERVICE_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("SERVICE_CORS_ALLOW_CREDENTIALS", "false")

    cfg = APISettings()

    assert cfg.cors.allow_credentials is False
    assert cfg.cors.origins == DEFAULT_LOCAL_CORS_ORIGINS


def test_service_cors_allows_wildcard_when_credentials_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SERVICE_CORS_ORIGINS", "*")
    monkeypatch.setenv("SERVICE_CORS_ALLOW_CREDENTIALS", "false")

    cfg = APISettings()

    assert cfg.cors.origins == ["*"]
    assert cfg.cors.allow_credentials is False


def test_service_cors_rejects_wildcard_with_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SERVICE_CORS_ORIGINS", "*")
    monkeypatch.setenv("SERVICE_CORS_ALLOW_CREDENTIALS", "true")

    with pytest.raises(ValueError, match="cannot contain '\\*'"):
        APISettings()


def test_service_cors_rejects_wildcard_with_common_truthy_credentials_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SERVICE_CORS_ORIGINS", "*")
    monkeypatch.setenv("SERVICE_CORS_ALLOW_CREDENTIALS", "yes")

    with pytest.raises(ValueError, match="cannot contain '\\*'"):
        APISettings()


def test_real_app_cors_denies_unlisted_external_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/healthz",
        headers={
            "Origin": "https://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


def test_real_app_cors_allows_default_local_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/healthz",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_real_app_cors_middleware_has_no_wildcard_credentialed_origin() -> None:
    cors_middleware = next(
        middleware
        for middleware in app.user_middleware
        if isinstance(middleware, Middleware) and middleware.cls.__name__ == "CORSMiddleware"
    )

    assert cors_middleware.kwargs["allow_credentials"] is True
    assert "*" not in cors_middleware.kwargs["allow_origins"]
