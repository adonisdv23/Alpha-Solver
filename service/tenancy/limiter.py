"""Per-tenant rate limiting utilities.

This module implements a very small in-memory token bucket limiter with an
optional daily quota.  It is intentionally lightweight and aimed at unit tests
and small deployments.  Configuration is sourced from a YAML file mapping tenant
ids to rate/quotas.  The configuration can be reloaded at runtime via
:meth:`TenantLimiter.reload_config`.
"""
from __future__ import annotations

import time
import datetime as _dt
from pathlib import Path
from typing import Dict, Tuple, Optional

import yaml


class TenantLimiter:
    """Token bucket limiter keyed by tenant id."""

    def __init__(self, config_path: Path | str):
        self.config_path = Path(config_path)
        self._config_mtime = 0.0
        self.default: Dict[str, float] = {
            "rate_per_sec": 1.0,
            "burst": 1.0,
            "quota_per_day": None,
        }
        self.tenants: Dict[str, Dict[str, float]] = {}
        # bucket state: tenant -> {tokens, last, quota_used, quota_day}
        self._buckets: Dict[str, Dict[str, float]] = {}
        # metrics and event log for observability and tests
        self.metrics: Dict[str, Dict[str, int]] = {}
        self.events: Dict[str, list] = {}
        self.load_config()

    # ------------------------------------------------------------------ config
    def load_config(self) -> None:
        """Load configuration from ``self.config_path``."""
        if not self.config_path.exists():
            self.tenants = {}
            return
        stat = self.config_path.stat()
        if stat.st_mtime <= self._config_mtime:
            return
        data = yaml.safe_load(self.config_path.read_text()) or {}
        self.default.update(data.get("default", {}))
        self.tenants = data.get("tenants", {})
        self._config_mtime = stat.st_mtime
        # reset existing buckets to new burst levels
        now = time.monotonic()
        for tenant, limits in self.tenants.items():
            bucket = self._buckets.get(tenant)
            if bucket:
                bucket["tokens"] = float(limits.get("burst", self.default["burst"]))
                bucket["last"] = now

    reload_config = load_config

    # ----------------------------------------------------------------- helpers
    def _limits_for(self, tenant_id: str) -> Dict[str, float]:
        cfg = {**self.default, **self.tenants.get(tenant_id, {})}
        return cfg

    def reset_quota(self, tenant_id: str) -> None:
        bucket = self._buckets.get(tenant_id)
        if bucket:
            bucket["quota_used"] = 0
            bucket["quota_day"] = _dt.date.today()

    # --------------------------------------------------------------- main API
    def allow_request(self, tenant_id: str) -> Tuple[bool, Optional[str]]:
        """Return ``(True, None)`` if request may proceed.

        When rejected a tuple ``(False, reason)`` is returned where ``reason`` is
        ``"rate_limited"`` or ``"quota_exceeded"``.
        """

        limits = self._limits_for(tenant_id)
        now = time.monotonic()
        bucket = self._buckets.setdefault(
            tenant_id,
            {
                "tokens": float(limits.get("burst", 1.0)),
                "last": now,
                "quota_used": 0,
                "quota_day": _dt.date.today(),
            },
        )
        elapsed = now - bucket["last"]
        bucket["last"] = now
        bucket["tokens"] = min(
            float(limits.get("burst", 1.0)),
            bucket["tokens"] + elapsed * float(limits.get("rate_per_sec", 0.0)),
        )

        # daily quota reset
        today = _dt.date.today()
        if bucket["quota_day"] != today:
            bucket["quota_day"] = today
            bucket["quota_used"] = 0

        # enforce quota
        qpd = limits.get("quota_per_day")
        if qpd is not None and bucket["quota_used"] >= float(qpd):
            self._record(tenant_id, False, "quota_exceeded")
            return False, "quota_exceeded"

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            bucket["quota_used"] += 1
            self._record(tenant_id, True, None)
            return True, None

        self._record(tenant_id, False, "rate_limited")
        return False, "rate_limited"

    # ------------------------------------------------------------- observability
    def _record(self, tenant_id: str, allowed: bool, reason: Optional[str]) -> None:
        m = self.metrics.setdefault(tenant_id, {"allowed": 0, "denied": 0})
        if allowed:
            m["allowed"] += 1
            action = "allow"
        else:
            m["denied"] += 1
            action = "deny"
        e = self.events.setdefault(tenant_id, [])
        e.append({"tenant": tenant_id, "action": action, "reason": reason})


__all__ = ["TenantLimiter"]
