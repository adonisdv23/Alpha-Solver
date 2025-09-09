from fastapi.testclient import TestClient

from service.app import app

client = TestClient(app)


def test_metrics_exposed():
    client.get("/healthz")
    res = client.get("/metrics")
    assert res.status_code == 200
    body = res.json()
    assert "alpha_requests_total" in body
    assert "alpha_request_latency_seconds" in body
    assert "alpha_ratelimit_total" in body
    assert "alpha_safe_out_total" in body
