from __future__ import annotations

import datetime as _dt
import json
import os
from typing import Any, Dict, Optional


class JsonlLogger:
    """Structured JSONL logger with simple size-based rotation."""

    def __init__(self, log_path: str, rotate_mb: int = 50, with_pid: bool = True) -> None:
        self.log_path = log_path
        self.rotate_bytes = rotate_mb * 1024 * 1024
        self.with_pid = with_pid
        self._pid = os.getpid() if with_pid else None
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        self._fp = open(self.log_path, "a", encoding="utf-8")

    # ------------------------------------------------------------------
    def _should_rotate(self) -> bool:
        try:
            return os.path.getsize(self.log_path) >= self.rotate_bytes
        except FileNotFoundError:
            return False

    def _rotate(self) -> None:
        self._fp.close()
        idx = 1
        while os.path.exists(f"{self.log_path}.{idx}"):
            idx += 1
        os.rename(self.log_path, f"{self.log_path}.{idx}")
        self._fp = open(self.log_path, "a", encoding="utf-8")

    # ------------------------------------------------------------------
    def event(
        self,
        *,
        name: str,
        route_explain: Dict[str, Any],
        payload: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a structured event to JSONL."""

        required = {"decision", "confidence", "budget_verdict"}
        missing = required - route_explain.keys()
        if missing:
            raise ValueError(f"route_explain missing keys: {sorted(missing)}")

        if self._should_rotate():
            self._rotate()

        clean_payload: Dict[str, Any] = {}
        if payload:
            clean_payload = {k: v for k, v in payload.items() if k != "pii_raw"}

        event = {
            "ts": _dt.datetime.utcnow().isoformat() + "Z",
            "pid": self._pid,
            "name": name,
            "route_explain": route_explain,
            "payload": clean_payload,
            "meta": meta or {},
        }

        line = json.dumps(event, separators=(",", ":"))
        self._fp.write(line + "\n")
        self._fp.flush()
        os.fsync(self._fp.fileno())

    # ------------------------------------------------------------------
    def close(self) -> None:
        """Flush and close underlying log file."""

        if not self._fp.closed:
            self._fp.flush()
            os.fsync(self._fp.fileno())
            self._fp.close()
