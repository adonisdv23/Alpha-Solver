import os
import uuid
import logging
from pathlib import Path

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

from fastapi.testclient import TestClient
from service.app import app


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


def test_cost_tracking(monkeypatch, caplog):
    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    path = Path("artifacts/costs.csv")
    if path.exists():
        path.unlink()
    caplog.set_level(logging.INFO)
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})
    assert resp.status_code == 200
    assert path.exists()
    with path.open() as fh:
        assert fh.readline()
    assert any(rec.getMessage() == "cost" for rec in caplog.records)
