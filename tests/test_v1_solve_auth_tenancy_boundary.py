import uuid

import pytest
from fastapi.testclient import TestClient

from service.app import app, time as service_time


@pytest.fixture(autouse=True)
def _restore_app_state(monkeypatch):
    original_keys = list(app.state.config.auth.keys)
    original_auth_enabled = app.state.config.auth.enabled
    original_rl_enabled = app.state.config.ratelimit.enabled
    original_window = app.state.config.ratelimit.window_seconds
    original_max = app.state.config.ratelimit.max_requests
    had_factory = hasattr(app.state, "provider_client_factory")
    original_factory = getattr(app.state, "provider_client_factory", None)
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    try:
        yield
    finally:
        app.state.config.auth.keys = original_keys
        app.state.config.auth.enabled = original_auth_enabled
        app.state.config.ratelimit.enabled = original_rl_enabled
        app.state.config.ratelimit.window_seconds = original_window
        app.state.config.ratelimit.max_requests = original_max
        if had_factory:
            app.state.provider_client_factory = original_factory
        elif hasattr(app.state, "provider_client_factory"):
            delattr(app.state, "provider_client_factory")


def _client(max_requests=10):
    key = f"synthetic-{uuid.uuid4()}"
    app.state.config.auth.enabled = True
    app.state.config.auth.keys = [key]
    app.state.config.ratelimit.enabled = True
    app.state.config.ratelimit.window_seconds = 60
    app.state.config.ratelimit.max_requests = max_requests
    return TestClient(app), key


def test_v1_solve_rejects_unauthorized_before_solver(monkeypatch):
    called = {"solver": False}

    def fail_solver(*args, **kwargs):
        called["solver"] = True
        raise AssertionError("solver should not run without auth")

    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr("service.app._tree_of_thought", fail_solver)
    client, _key = _client()

    response = client.post("/v1/solve", json={"query": "hello"})

    assert response.status_code == 401
    assert response.json()["final_answer"] == "SAFE-OUT: invalid API key"
    assert called["solver"] is False


def test_v1_solve_authorized_local_request_does_not_call_provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr(
        "service.app._tree_of_thought",
        lambda query, **kwargs: {"final_answer": f"local:{query}", "meta": kwargs},
    )
    app.state.provider_client_factory = lambda _model_set: (_ for _ in ()).throw(
        AssertionError("provider should not be constructed in local mode")
    )
    client, key = _client()

    response = client.post(
        "/v1/solve",
        json={"query": "hello", "context": {"tenant": "tenant-a", "route": "expert"}},
        headers={"X-API-Key": key, "X-Tenant-ID": "tenant-a"},
    )

    assert response.status_code == 200
    assert response.json()["final_answer"] == "local:hello"
    assert "route" not in response.json()["meta"]


def test_v1_solve_rate_limit_is_per_api_key_not_tenant(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {"final_answer": "ok"})
    now = [100.0]
    monkeypatch.setattr(service_time, "time", lambda: now[0])
    client, key = _client(max_requests=1)

    first = client.post(
        "/v1/solve",
        json={"query": "hello"},
        headers={"X-API-Key": key, "X-Tenant-ID": "tenant-a"},
    )
    second = client.post(
        "/v1/solve",
        json={"query": "hello"},
        headers={"X-API-Key": key, "X-Tenant-ID": "tenant-b"},
    )

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json()["final_answer"] == "SAFE-OUT: rate limit exceeded"


def test_v1_solve_cors_allows_configured_local_origin_with_credentials():
    client, key = _client()

    response = client.options(
        "/v1/solve",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key, Content-Type",
            "X-API-Key": key,
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_v1_solve_cors_rejects_unconfigured_origin():
    client, key = _client()

    response = client.options(
        "/v1/solve",
        headers={
            "Origin": "https://example.invalid",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key, Content-Type",
            "X-API-Key": key,
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
