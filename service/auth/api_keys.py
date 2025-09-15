"""API key management utilities."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set

import yaml


@dataclass
class APIKey:
    """Represents a single API key entry loaded from config."""

    id: str
    hash: str  # stored as "<salt>$<digest>"
    tenant_id: str
    scopes: Set[str]
    status: str
    created_at: float

    def verify(self, raw: str) -> bool:
        """Verify a raw key against this entry's salted hash."""
        try:
            salt, digest = self.hash.split("$", 1)
        except ValueError:  # pragma: no cover - config error
            return False
        check = hashlib.sha256((salt + raw).encode()).hexdigest()
        return secrets.compare_digest(check, digest)


def hash_key(key: str, salt: str | None = None) -> str:
    """Return a salt$digest string for the given key."""
    salt = salt or secrets.token_hex(8)
    digest = hashlib.sha256((salt + key).encode()).hexdigest()
    return f"{salt}${digest}"


class APIKeyStore:
    """Simple YAML-backed API key store."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._mtime: float = 0.0
        self._keys: List[APIKey] = []
        self.reload(force=True)

    def reload(self, force: bool = False) -> None:
        try:
            mtime = self.path.stat().st_mtime
        except FileNotFoundError:
            self._keys = []
            self._mtime = 0.0
            return
        if not force and mtime == self._mtime:
            return
        data = yaml.safe_load(self.path.read_text()) or {}
        items = []
        for item in data.get("keys", []):
            if not item:
                continue
            scopes = set(item.get("scopes") or [])
            items.append(
                APIKey(
                    id=str(item.get("id")),
                    hash=str(item.get("hash")),
                    tenant_id=str(item.get("tenant_id") or ""),
                    scopes=scopes,
                    status=str(item.get("status") or "active"),
                    created_at=float(item.get("created_at") or 0),
                )
            )
        self._keys = items
        self._mtime = mtime

    def match_key(self, raw_key: str) -> Optional[APIKey]:
        """Return the key matching the raw value regardless of status."""
        self.reload()
        for entry in self._keys:
            if entry.verify(raw_key):
                return entry
        return None

    def find_key(self, raw_key: str) -> Optional[APIKey]:
        """Return the APIKey if it matches and is active."""
        entry = self.match_key(raw_key)
        if entry and entry.status == "active":
            return entry
        return None

    def get(self, key_id: str) -> Optional[APIKey]:
        """Return the key by id regardless of status."""
        self.reload()
        for entry in self._keys:
            if entry.id == key_id:
                return entry
        return None


__all__ = ["APIKey", "APIKeyStore", "hash_key"]
