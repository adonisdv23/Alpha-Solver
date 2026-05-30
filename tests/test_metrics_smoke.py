from fastapi.testclient import TestClient

from alpha.core.telemetry import record_rate_limit, record_safe_out
from service.app import app

client = TestClient(app)


def test_metrics_exposed():
    client.get("/healthz")
    record_rate_limit("/metrics-smoke")
    record_safe_out("/metrics-smoke")
    res = client.get("/metrics")
    assert res.status_code == 200
    body = res.json()
    assert "alpha_requests_total" in body
    assert "alpha_request_latency_seconds" in body
    assert "alpha_ratelimit_total" in body
    assert "alpha_safe_out_total" in body
