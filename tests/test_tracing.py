import os
import uuid

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

from fastapi.testclient import TestClient
from service.app import app
from service.otel import init_tracer
try:
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
except ImportError:
    from opentelemetry.sdk.trace.export import InMemorySpanExporter
from opentelemetry import trace


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


def test_tracing(monkeypatch):
    exporter = InMemorySpanExporter()
    init_tracer(app, exporter)  # re-initialise with in-memory exporter

    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})
    assert resp.status_code == 200
    assert "X-Request-ID" in resp.headers
    trace.get_tracer_provider().force_flush()  # ensure spans exported
    spans = exporter.get_finished_spans()
    assert spans
