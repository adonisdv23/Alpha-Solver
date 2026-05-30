from pathlib import Path

import yaml

from service.tenancy.limiter import TenantLimiter


def test_tenant_limiter_uses_in_memory_token_bucket(tmp_path: Path):
    cfg_path = tmp_path / "tenants.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "default": {"rate_per_sec": 0, "burst": 1},
                "tenants": {"tenant-a": {"rate_per_sec": 0, "burst": 1}},
            }
        )
    )
    limiter = TenantLimiter(cfg_path)

    assert limiter.allow_request("tenant-a") == (True, None)
    assert limiter.allow_request("tenant-a") == (False, "rate_limited")
    assert "tenant-a" in limiter._buckets
    assert limiter.metrics["tenant-a"] == {"allowed": 1, "denied": 1}


def test_tenant_limiter_enforces_in_memory_quota(tmp_path: Path):
    cfg_path = tmp_path / "tenants.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "default": {"rate_per_sec": 10, "burst": 10},
                "tenants": {"tenant-b": {"quota_per_day": 1}},
            }
        )
    )
    limiter = TenantLimiter(cfg_path)

    assert limiter.allow_request("tenant-b") == (True, None)
    assert limiter.allow_request("tenant-b") == (False, "quota_exceeded")
    assert limiter.events["tenant-b"][-1] == {
        "tenant": "tenant-b",
        "action": "deny",
        "reason": "quota_exceeded",
    }
