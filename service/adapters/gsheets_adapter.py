from __future__ import annotations

"""Simulated Google Sheets adapter with basic hardening."""

from time import perf_counter, sleep
from typing import Any, Dict, List, Tuple

from .base import AdapterError, IToolAdapter


class GSheetsAdapter:
    """In-memory sheet store with idempotent appends and retries."""

    _LATENCY_S = 0.002

    def __init__(self) -> None:
        self._sheets: Dict[str, List[List[Any]]] = {}
        # key -> stored value for idempotent replies
        self._idem: Dict[
            Tuple[str, str, str | None, Tuple[Tuple[Any, ...], ...]],
            Dict[str, Any],
        ] = {}
        # track keys already forced to fail once for transient simulation
        self._transient_once: set[
            Tuple[str, str, Tuple[Tuple[Any, ...], ...]]
        ] = set()

    # Protocol methods -------------------------------------------------------
    def name(self) -> str:  # pragma: no cover - trivial
        return "gsheets"

    def _run_once(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise AdapterError(code="SCHEMA", retryable=False)

        # Merge idempotency sources (parameter takes precedence)
        idempotency_key = idempotency_key or payload.get("idempotency_key")

        # Drop any *_pii keys
        payload = {k: v for k, v in payload.items() if not k.endswith("_pii")}

        sheet = payload.get("sheet")
        cell_range = payload.get("range", "A1")
        op = payload.get("op")
        values = payload.get("values")

        if not isinstance(sheet, str) or op not in {"append", "read"}:
            raise AdapterError(code="SCHEMA", retryable=False)

        latency = self._LATENCY_S
        if timeout_s < latency:
            raise AdapterError(code="TIMEOUT", retryable=True)

        if op == "append":
            if not isinstance(values, list) or not all(isinstance(r, list) for r in values):
                raise AdapterError(code="SCHEMA", retryable=False)
            sanitized_values, sanitized_cells = self._sanitize_values(values)
            # simulate a flaky transient error on first unique payload
            transient_key = (
                sheet,
                cell_range,
                tuple(tuple(r) for r in sanitized_values),
            )
            if transient_key not in self._transient_once:
                self._transient_once.add(transient_key)
                raise AdapterError(code="TRANSIENT", retryable=True)
            idem_key = (
                sheet,
                cell_range,
                idempotency_key,
                tuple(tuple(r) for r in sanitized_values),
            )

            if idempotency_key and idem_key in self._idem:
                return self._idem[idem_key]

            rows = self._sheets.setdefault(sheet, [])
            rows.extend([list(r) for r in sanitized_values])
            value = len(sanitized_values)
            start = perf_counter()
            end = perf_counter()
            meta = {
                "latency_ms": (end - start) * 1000,
                "attempts": 1,
                "idempotent": False,
                "sanitized_cells": sanitized_cells,
                "retryable": False,
            }
            res = {"ok": True, "value": value, "meta": meta}
            if idempotency_key:
                self._idem[idem_key] = res
            return res

        else:  # read
            start = perf_counter()
            sleep(latency)
            rows = self._sheets.get(sheet, [])
            value = [list(r) for r in rows]
            end = perf_counter()
            meta = {
                "latency_ms": (end - start) * 1000,
                "attempts": 1,
                "idempotent": True,
                "sanitized_cells": 0,
                "retryable": False,
            }
            return {"ok": True, "value": value, "meta": meta}

    def run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        from .base_adapter import call_adapter

        # treat operations as safe to retry since _run_once raises before mutation
        idem = True
        return call_adapter(
            lambda: self._run_once(payload, idempotency_key=idempotency_key, timeout_s=timeout_s),
            adapter=self.name(),
            idempotent=idem,
        )

    def _sanitize_values(self, values: List[List[Any]]) -> Tuple[List[List[Any]], int]:
        sanitized: List[List[Any]] = []
        changed = 0
        for row in values:
            new_row: List[Any] = []
            for cell in row:
                orig = cell
                if isinstance(cell, str):
                    cell = cell.strip().replace("\n", "")
                new_row.append(cell)
                if cell != orig:
                    changed += 1
            sanitized.append(new_row)
        return sanitized, changed

    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": self.name(),
            "latency_ms": float(meta.get("latency_ms", 0.0)),
            "attempts": int(meta.get("attempts", 1)),
            "idempotent": bool(meta.get("idempotent", False)),
            "sanitized_cells": int(meta.get("sanitized_cells", 0)),
            "retriable": bool(meta.get("retryable", meta.get("retriable", False))),
        }

