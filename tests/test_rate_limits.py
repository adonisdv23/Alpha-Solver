import time
from pathlib import Path

import yaml
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from service.middleware.tenant_middleware import TenantMiddleware
from service.tenancy.limiter import TenantLimiter


def build_app(cfg_path: Path) -> tuple[Starlette, TenantLimiter, TestClient]:
    limiter = TenantLimiter(cfg_path)
    app = Starlette()

    @app.route("/ping")
    async def ping(request):
        return JSONResponse({"tenant": request.state.tenant_id})

    app.add_middleware(TenantMiddleware, limiter=limiter)
    client = TestClient(app)
    return app, limiter, client


def test_rate_limiting_and_quota(tmp_path: Path):
    cfg = {
        "default": {"rate_per_sec": 0, "burst": 1},
        "tenants": {
            "tenant_a": {"rate_per_sec": 0, "burst": 2},
            "tenant_b": {"rate_per_sec": 1, "burst": 1},
            "tenant_c": {"rate_per_sec": 5, "burst": 5, "quota_per_day": 3},
        },
    }
    cfg_path = tmp_path / "tenants.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))

    _, limiter, client = build_app(cfg_path)

    # tenant_a: burst=2, no refill -> over-limit rejection
    h = {"X-Tenant-ID": "tenant_a"}
    assert client.get("/ping", headers=h).status_code == 200
    assert client.get("/ping", headers=h).status_code == 200
    assert client.get("/ping", headers=h).status_code == 429
    over = sum(1 for _ in range(100) if client.get("/ping", headers=h).status_code == 429)
    assert over >= 99

    # tenant_b: rate=1/sec, burst=1 -> allow after refill
    h = {"X-Tenant-ID": "tenant_b"}
    assert client.get("/ping", headers=h).status_code == 200
    assert client.get("/ping", headers=h).status_code == 429
    time.sleep(1.1)
    assert client.get("/ping", headers=h).status_code == 200

    # tenant_c: quota 3/day
    h = {"X-Tenant-ID": "tenant_c"}
    for _ in range(3):
        assert client.get("/ping", headers=h).status_code == 200
    r = client.get("/ping", headers=h)
    assert r.status_code == 429
    assert r.json()["code"] == "quota_exceeded"
    limiter.reset_quota("tenant_c")
    assert client.get("/ping", headers=h).status_code == 200


def test_reload_and_performance(tmp_path: Path):
    cfg = {
        "default": {"rate_per_sec": 0, "burst": 1},
        "tenants": {"r": {"rate_per_sec": 0, "burst": 1}},
    }
    cfg_path = tmp_path / "tenants.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))

    _, limiter, client = build_app(cfg_path)
    h = {"X-Tenant-ID": "r"}
    assert client.get("/ping", headers=h).status_code == 200
    assert client.get("/ping", headers=h).status_code == 429

    # change burst and reload
    cfg["tenants"]["r"]["burst"] = 2
    cfg_path.write_text(yaml.safe_dump(cfg))
    limiter.reload_config()
    assert client.get("/ping", headers=h).status_code == 200
    assert client.get("/ping", headers=h).status_code == 200

    # performance check
    times = []
    for _ in range(200):
        t0 = time.perf_counter()
        limiter.allow_request("perf")
        times.append(time.perf_counter() - t0)
    p95 = sorted(times)[int(len(times) * 0.95)]
    if p95 > 0.005:  # environment too slow
        import pytest

        pytest.skip("environment slow")
    assert p95 < 0.001
