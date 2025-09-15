import yaml
from pathlib import Path
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from service.middleware.tenant_middleware import TenantMiddleware
from service.tenancy.limiter import TenantLimiter


def build_app(cfg_path: Path) -> tuple[Starlette, TenantLimiter]:
    limiter = TenantLimiter(cfg_path)
    app = Starlette()

    @app.route("/ping")
    async def ping(request):
        return JSONResponse({"tenant": request.state.tenant_id})

    app.add_middleware(TenantMiddleware, limiter=limiter)
    return app, limiter


def test_tenant_isolation(tmp_path: Path):
    cfg = {
        "default": {"rate_per_sec": 10, "burst": 10},
        "tenants": {"A": {}, "B": {}, "C": {}},
    }
    cfg_path = tmp_path / "tenants.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))

    app, limiter = build_app(cfg_path)
    client = TestClient(app)
    tenants = ["A", "B", "C"]
    for t in tenants:
        r = client.get("/ping", headers={"X-Tenant-ID": t})
        assert r.status_code == 200
        assert r.json()["tenant"] == t

    # ensure metrics/logs are segregated per tenant
    for t in tenants:
        assert limiter.metrics[t]["allowed"] == 1
        assert limiter.metrics[t]["denied"] == 0
        assert all(ev["tenant"] == t for ev in limiter.events[t])
