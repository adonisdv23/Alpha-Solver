import os
import os
import os
import uuid
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

# Avoid binding the Prometheus port during import
with patch("prometheus_client.start_http_server", lambda *a, **k: None):
    from service.app import app

import service.otel as otel


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


@pytest.mark.skipif(not otel.HAVE_OTEL, reason="OpenTelemetry not installed")
def test_tracing(monkeypatch):
    from opentelemetry import trace
    from opentelemetry.sdk.trace.export import InMemorySpanExporter

    exporter = InMemorySpanExporter()
    otel.init_tracer(app, exporter)

    client, key = _client()
    monkeypatch.setattr("service.app._tree_of_thought", lambda *a, **k: {})
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})
    assert resp.status_code == 200
    assert "X-Request-ID" in resp.headers
    trace.get_tracer_provider().force_flush()
    spans = exporter.get_finished_spans()
    assert spans


def test_noop_tracer_when_missing(monkeypatch):
    monkeypatch.setattr(otel, "HAVE_OTEL", False)
    dummy = SimpleNamespace(state=SimpleNamespace())
    tracer = otel.init_tracer(dummy)
    assert isinstance(tracer, otel._NoopTracer)
