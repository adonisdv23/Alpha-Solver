import os
import uuid

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


def test_health_ready_and_openapi():
    client, key = _client()
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/metrics").status_code == 200


def test_solve_endpoint(monkeypatch):
    client, key = _client()

    def fake_solver(query: str, **kwargs):
        return {"final_answer": "ok"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})
    assert resp.status_code == 200
    assert resp.json()["final_answer"] == "ok"


def test_solve_endpoint_react(monkeypatch):
    client, key = _client()

    def fake_react(prompt: str, seed: int, max_steps: int = 2, rules=None):
        return {"final_answer": "ok", "trace": [], "confidence": 0.9, "meta": {"strategy": "react", "seed": seed}}

    monkeypatch.setattr("alpha.reasoning.react_lite.run_react_lite", fake_react)
    resp = client.post(
        "/v1/solve",
        json={"query": "hi", "strategy": "react"},
        headers={"X-API-Key": key},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["final_answer"] == "ok"
    assert body["meta"]["strategy"] == "react"
