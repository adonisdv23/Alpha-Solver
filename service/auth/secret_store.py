from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Dict, Tuple

import yaml


class SecretStore:
    """Simple versioned secret store backed by YAML data."""

    def __init__(self, path: Path | str | None = None, data: dict | None = None) -> None:
        if data is None:
            if path is None:
                raise ValueError("path or data required")
            data = yaml.safe_load(Path(path).read_text()) or {}
        self._store: Dict[Tuple[str, str], Dict[str, object]] = {}
        for item in data.get("secrets", []):
            provider = item.get("provider")
            tenant = item.get("tenant_id")
            if not provider or not tenant:
                # allow "id" as "provider-tenant"
                pid = item.get("id", "-")
                provider, tenant = pid.split("-", 1)
            version = item["version"]
            key = (provider, tenant)
            entry = self._store.setdefault(key, {"current": version, "versions": {}, "previous": None})
            entry["versions"][version] = {k: v for k, v in item.items() if k not in {"provider", "tenant_id", "id"}}
            entry["current"] = version

    # ------------------------------------------------------------------
    def get(self, provider: str, tenant_id: str, version: str | None = None) -> dict:
        """Return a copy of the secret for provider/tenant/version."""
        entry = self._store[(provider, tenant_id)]
        ver = version or entry["current"]
        return deepcopy(entry["versions"][ver])

    def set(self, provider: str, tenant_id: str, secret: dict) -> None:
        """Rotate to a new secret version."""
        version = secret["version"]
        key = (provider, tenant_id)
        entry = self._store.setdefault(key, {"current": version, "versions": {}, "previous": None})
        entry["previous"] = entry.get("current")
        entry["versions"][version] = {k: v for k, v in secret.items() if k not in {"provider", "tenant_id"}}
        entry["current"] = version

    def rollback(self, provider: str, tenant_id: str) -> None:
        key = (provider, tenant_id)
        entry = self._store[key]
        prev = entry.get("previous")
        if prev:
            entry["current"], entry["previous"] = prev, entry["current"]

    # ------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover - repr only for debugging
        keys = [f"{p}:{t}" for (p, t) in self._store.keys()]
        return f"<SecretStore keys={keys}>"


__all__ = ["SecretStore"]
