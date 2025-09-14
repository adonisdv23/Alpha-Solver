from __future__ import annotations

"""Simulated Google Sheets adapter."""

from time import perf_counter, sleep
from typing import Any, Dict, List, Tuple

from .base import AdapterError, IToolAdapter


class GSheetsAdapter:
    """In-memory sheet store with idempotent appends."""

    _LATENCY_S = 0.002

    def __init__(self) -> None:
        self._sheets: Dict[str, List[List[Any]]] = {}
        self._idem: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}

    def name(self) -> str:  # pragma: no cover - trivial
        return "gsheets"

    def run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        if idempotency_key and idempotency_key in self._idem:
            prev_payload, prev_res = self._idem[idempotency_key]
            if prev_payload == payload:
                return prev_res
            raise AdapterError(code="SCHEMA", retryable=False)

        if not isinstance(payload, dict):
            raise AdapterError(code="SCHEMA", retryable=False)
        sheet = payload.get("sheet")
        op = payload.get("op")
        values = payload.get("values")
        if not isinstance(sheet, str) or op not in {"append", "read"}:
            raise AdapterError(code="SCHEMA", retryable=False)

        latency = self._LATENCY_S
        if timeout_s < latency:
            raise AdapterError(code="TIMEOUT", retryable=True)

        start = perf_counter()
        sleep(latency)
        if op == "append":
            if not isinstance(values, list) or not all(isinstance(r, list) for r in values):
                raise AdapterError(code="SCHEMA", retryable=False)
            rows = self._sheets.setdefault(sheet, [])
            rows.extend([list(r) for r in values])
            value: Any = len(values)
        else:  # read
            rows = self._sheets.get(sheet, [])
            value = [list(r) for r in rows]
        end = perf_counter()
        meta = {"latency_ms": (end - start) * 1000, "retryable": False}
        res = {"ok": True, "value": value, "meta": meta}
        if op == "append" and idempotency_key:
            self._idem[idempotency_key] = (payload, res)
        return res

    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": self.name(),
            "latency_ms": float(meta.get("latency_ms", 0.0)),
            "attempts": 1,
            "retriable": bool(meta.get("retryable", meta.get("retriable", False))),
        }
