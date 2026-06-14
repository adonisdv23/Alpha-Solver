import uuid

from fastapi.testclient import TestClient

from service.app import _REQUESTS, app, time as service_time


def _configure_boundary(max_requests=10):
    key = f"test-{uuid.uuid4()}"
    app.state.config.auth.enabled = True
    app.state.config.auth.header = "X-API-Key"
    app.state.config.auth.keys = [key]
    app.state.config.ratelimit.enabled = True
    app.state.config.ratelimit.window_seconds = 60
    app.state.config.ratelimit.max_requests = max_requests
    _REQUESTS.clear()
    return TestClient(app), key


def test_unauthorized_v1_solve_fails_before_solver_execution(monkeypatch):
    client, _key = _configure_boundary()
    solver_called = False

    def fail_solver(*args, **kwargs):
        nonlocal solver_called
        solver_called = True
        raise AssertionError("solver must not run for unauthorized requests")

    monkeypatch.setattr("service.app._tree_of_thought", fail_solver)

    resp = client.post("/v1/solve", json={"query": "local boundary"})

    assert resp.status_code == 401
    assert resp.json()["final_answer"].startswith("SAFE-OUT")
    assert solver_called is False


def test_authorized_local_request_does_not_construct_provider_client(monkeypatch):
    client, key = _configure_boundary()
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    monkeypatch.setattr(
        "service.app._tree_of_thought",
        lambda query, **kwargs: {"final_answer": f"local:{query}"},
    )

    def fail_provider_factory(*args, **kwargs):
        raise AssertionError("provider client must not be constructed for local provider")

    app.state.provider_client_factory = fail_provider_factory
    try:
        resp = client.post(
            "/v1/solve",
            json={"query": "local only"},
            headers={"X-API-Key": key},
        )
    finally:
        if hasattr(app.state, "provider_client_factory"):
            delattr(app.state, "provider_client_factory")

    assert resp.status_code == 200
    assert resp.json()["final_answer"] == "local:local only"


def test_rate_limit_is_api_key_scoped(monkeypatch):
    client, key_one = _configure_boundary(max_requests=1)
    key_two = f"test-{uuid.uuid4()}"
    app.state.config.auth.keys = [key_one, key_two]
    monkeypatch.setattr(
        "service.app._tree_of_thought",
        lambda query, **kwargs: {"final_answer": query},
    )
    now = [100.0]
    monkeypatch.setattr(service_time, "time", lambda: now[0])

    first = client.post("/v1/solve", json={"query": "one"}, headers={"X-API-Key": key_one})
    limited = client.post("/v1/solve", json={"query": "one again"}, headers={"X-API-Key": key_one})
    other_key = client.post("/v1/solve", json={"query": "two"}, headers={"X-API-Key": key_two})

    assert first.status_code == 200
    assert limited.status_code == 429
    assert other_key.status_code == 200


def test_cors_preflight_inherits_main_cors_configuration():
    client, _key = _configure_boundary()

    resp = client.options(
        "/v1/solve",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key,Content-Type",
        },
    )

    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in resp.headers["access-control-allow-methods"]


def test_local_boundary_makes_no_provider_call(monkeypatch):
    client, key = _configure_boundary()
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    provider_called = False

    def fake_execute_provider_call(*args, **kwargs):
        nonlocal provider_called
        provider_called = True
        raise AssertionError("provider call must not run in local boundary test")

    monkeypatch.setattr("service.app._execute_provider_call", fake_execute_provider_call)
    monkeypatch.setattr(
        "service.app._tree_of_thought",
        lambda query, **kwargs: {"final_answer": "local evidence"},
    )

    resp = client.post(
        "/v1/solve",
        json={"query": "no provider"},
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    assert resp.json()["final_answer"] == "local evidence"
    assert provider_called is False
