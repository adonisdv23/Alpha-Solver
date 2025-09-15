import re
import time

import pytest
from fastapi.testclient import TestClient

from service.metrics.testing import reset_registry
from service.app import app


@pytest.fixture()
def client():
    reset_registry()
    return TestClient(app)


def test_metrics_smoke(client):
    t0 = time.perf_counter()
    client.get("/healthz")
    res = client.get("/metrics")
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert res.status_code == 200
    assert elapsed_ms < 200
    assert (
        res.headers.get("content-type")
        == "text/plain; version=0.0.4; charset=utf-8"
    )
    text = res.text
    for name in [
        "alpha_solver_route_decision_total",
        "alpha_solver_budget_verdict_total",
        "alpha_solver_latency_ms_bucket",
        "alpha_solver_tokens_total",
        "alpha_solver_cost_usd_total",
    ]:
        assert name in text
    # basic PII/secret scan
    assert not re.search(r"(api|auth)_token|secret|@|\d{3}-\d{3}-\d{4}", text, re.I)
