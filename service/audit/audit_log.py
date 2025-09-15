import re
import threading
import time
from typing import Any, Dict, Iterable, List, Optional

from .hash_chain import ZERO_HASH, compute_hash, verify_chain


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
_TOKEN_RE = re.compile(r"\b(?:token|secret|password)[A-Za-z0-9_-]*\b", re.I)


class AuditLog:
    def __init__(
        self,
        retention_days: int = 30,
        enabled_event_types: Optional[List[str]] = None,
    ) -> None:
        self.retention_seconds = retention_days * 24 * 3600
        self.enabled_event_types = enabled_event_types
        self._entries: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    # --- redaction -----------------------------------------------------
    def _redact(self, value: Any) -> Any:
        if isinstance(value, str):
            value = _EMAIL_RE.sub("[REDACTED]", value)
            value = _PHONE_RE.sub("[REDACTED]", value)
            value = _TOKEN_RE.sub("[REDACTED]", value)
            return value
        if isinstance(value, dict):
            return {k: self._redact(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._redact(v) for v in value]
        return value

    # --- retention -----------------------------------------------------
    def _enforce_retention(self) -> None:
        cutoff = time.time() - self.retention_seconds
        removed = False
        while self._entries and self._entries[0]["ts"] < cutoff:
            self._entries.pop(0)
            removed = True
        if removed:
            prev = ZERO_HASH
            for entry in self._entries:
                entry["prev_hash"] = prev
                body = {k: v for k, v in entry.items() if k != "hash"}
                entry["hash"] = compute_hash(body, prev)
                prev = entry["hash"]

    # --- public API ----------------------------------------------------
    def record(self, event_type: str, payload: Dict[str, Any], ctx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self.enabled_event_types and event_type not in self.enabled_event_types:
            return None
        ts = time.time()
        with self._lock:
            entry_id = len(self._entries) + 1
            tenant_id = ctx.get("principal", {}).get("tenant_id")
            prev_hash = self._entries[-1]["hash"] if self._entries else ZERO_HASH
            body = {
                "ts": ts,
                "id": entry_id,
                "tenant_id": tenant_id,
                "type": event_type,
                "payload": self._redact(payload),
                "prev_hash": prev_hash,
            }
            entry_hash = compute_hash(body, prev_hash)
            entry = {**body, "hash": entry_hash}
            self._entries.append(entry)
            self._enforce_retention()
            return entry

    def iter_entries(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._entries)


_audit_log = AuditLog()


def record(event_type: str, payload: Dict[str, Any], ctx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _audit_log.record(event_type, payload, ctx)


def verify(stream: Iterable[Dict[str, Any]]) -> Optional[int]:
    return verify_chain(stream)
