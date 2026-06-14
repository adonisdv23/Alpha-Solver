from __future__ import annotations

import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from alpha.core.config import APISettings, ServiceAuthConfig, _load_service_auth_keys
from alpha.webapp.routes import auth as dashboard_auth
from service.app import app


def test_load_service_auth_keys_has_no_builtin_fallback(monkeypatch) -> None:
    monkeypatch.delenv("SERVICE_AUTH_KEYS", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)

    assert _load_service_auth_keys() == []
    assert ServiceAuthConfig().keys == []


def test_load_service_auth_keys_accepts_explicit_synthetic_values(monkeypatch) -> None:
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.setenv("SERVICE_AUTH_KEYS", " synthetic-one, synthetic-two ,, ")

    assert _load_service_auth_keys() == ["synthetic-one", "synthetic-two"]
    assert APISettings().auth.keys == ["synthetic-one", "synthetic-two"]


def test_api_key_env_accepts_explicit_synthetic_value(monkeypatch) -> None:
    key = f"synthetic-{uuid.uuid4()}"
    monkeypatch.delenv("SERVICE_AUTH_KEYS", raising=False)
    monkeypatch.setenv("API_KEY", key)

    assert _load_service_auth_keys() == [key]
    assert APISettings().auth.keys == [key]


def test_compose_files_do_not_inject_changeme_default() -> None:
    compose_paths = [
        Path("infrastructure/docker-compose.yml"),
        Path("infrastructure/docker-compose.prod.yml"),
    ]

    for path in compose_paths:
        text = path.read_text(encoding="utf-8")
        assert "API_KEY=${API_KEY:-changeme}" not in text
        assert "changeme" not in text
        assert "API_KEY=${API_KEY:?" in text


def test_missing_keys_fail_closed_for_protected_api_route(monkeypatch) -> None:
    original_keys = list(app.state.config.auth.keys)
    original_enabled = app.state.config.auth.enabled
    original_ratelimit = app.state.config.ratelimit.enabled
    app.state.config.auth.keys = []
    app.state.config.auth.enabled = True
    app.state.config.ratelimit.enabled = False
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {"final_answer": "ok"})

    try:
        response = TestClient(app).post("/v1/solve", json={"query": "hi"})
        assert response.status_code == 401
        assert response.json()["final_answer"].startswith("SAFE-OUT")
    finally:
        app.state.config.auth.keys = original_keys
        app.state.config.auth.enabled = original_enabled
        app.state.config.ratelimit.enabled = original_ratelimit


def test_explicit_synthetic_key_still_allows_protected_api_route(monkeypatch) -> None:
    key = f"synthetic-{uuid.uuid4()}"
    original_keys = list(app.state.config.auth.keys)
    original_enabled = app.state.config.auth.enabled
    original_ratelimit = app.state.config.ratelimit.enabled
    app.state.config.auth.keys = [key]
    app.state.config.auth.enabled = True
    app.state.config.ratelimit.enabled = False
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {"final_answer": "ok"})

    try:
        response = TestClient(app).post(
            "/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key}
        )
        assert response.status_code == 200
        assert response.json()["final_answer"] == "ok"
    finally:
        app.state.config.auth.keys = original_keys
        app.state.config.auth.enabled = original_enabled
        app.state.config.ratelimit.enabled = original_ratelimit


def test_dashboard_default_password_remains_fail_closed_for_real_app(monkeypatch) -> None:
    monkeypatch.setenv(dashboard_auth.PASSWORD_ENV_VAR, dashboard_auth.DEFAULT_DASHBOARD_PASSWORD)
    monkeypatch.setenv(dashboard_auth.SECRET_ENV_VAR, "unit-test-secret")

    from service.app import _dashboard_enabled

    assert _dashboard_enabled() is False
