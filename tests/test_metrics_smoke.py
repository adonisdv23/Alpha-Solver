from fastapi.testclient import TestClient
from service.app import app


def test_metrics_smoke():
    client = TestClient(app)
    client.get("/healthz")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    data = resp.text
    assert "alpha_request_total" in data
    assert "alpha_request_latency_ms" in data
    assert "alpha_rate_limit_total" in data
    assert "alpha_safe_out_total" in data
