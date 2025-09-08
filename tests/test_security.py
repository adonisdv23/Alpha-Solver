import os
import uuid

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

from fastapi.testclient import TestClient
from service.app import app


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


def test_missing_api_key(monkeypatch):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"})
    assert resp.status_code == 401


def test_invalid_api_key(monkeypatch):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401


def test_injection_rejected(monkeypatch):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "import os"}, headers={"X-API-Key": key})
    assert resp.status_code == 400
