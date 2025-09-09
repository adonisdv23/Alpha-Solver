import uuid

from fastapi.testclient import TestClient

from service.app import app, time as service_time


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    app.state.config.ratelimit.window_seconds = 60
    app.state.config.ratelimit.max_requests = 2
    return TestClient(app), key


def test_missing_api_key(monkeypatch):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"})
    assert resp.status_code == 401
    assert resp.json()["final_answer"].startswith("SAFE-OUT")


def test_invalid_api_key(monkeypatch):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": "bad"})
    assert resp.status_code == 401


def test_rate_limit_window(monkeypatch):
    client, key = _client()
    headers = {"X-API-Key": key}

    # deterministic time progression
    now = [0.0]

    def _time():
        return now[0]

    monkeypatch.setattr(service_time, "time", _time)
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})

    for _ in range(2):
        resp = client.post("/v1/solve", json={"query": "hi"}, headers=headers)
        assert resp.status_code == 200
        now[0] += 1

    resp = client.post("/v1/solve", json={"query": "hi"}, headers=headers)
    assert resp.status_code == 429

    # advance beyond window, should succeed
    now[0] += 61
    resp = client.post("/v1/solve", json={"query": "hi"}, headers=headers)
    assert resp.status_code == 200
