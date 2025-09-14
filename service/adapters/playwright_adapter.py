from __future__ import annotations

"""Simulated Playwright adapter."""

from time import perf_counter, sleep
from typing import Any, Dict, Tuple

from .base import AdapterError, IToolAdapter


class PlaywrightAdapter:
    """Tiny in-memory browser emulator."""

    _LATENCY_S = 0.005

    def __init__(self) -> None:
        self._pages: Dict[str, Dict[str, Any]] = {
            "https://example.com": {"text": "Example Domain", "clicks": 0}
        }
        self._idem: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}

    # Protocol methods -------------------------------------------------
    def name(self) -> str:  # pragma: no cover - trivial
        return "playwright"

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
        url = payload.get("url")
        action = payload.get("action")
        if not isinstance(url, str) or action not in {"get_text", "click", "screenshot"}:
            raise AdapterError(code="SCHEMA", retryable=False)

        latency = self._LATENCY_S
        if timeout_s < latency:
            raise AdapterError(code="TIMEOUT", retryable=True)

        start = perf_counter()
        sleep(latency)
        page = self._pages.setdefault(url, {"text": "", "clicks": 0})
        if action == "get_text":
            value: Any = page.get("text", "")
        elif action == "click":
            page["clicks"] = page.get("clicks", 0) + 1
            value = page["clicks"]
        else:  # screenshot
            value = f"screenshot:{url}"
        end = perf_counter()
        meta = {"url": url, "latency_ms": (end - start) * 1000, "retryable": False}
        res = {"ok": True, "value": value, "meta": meta}
        if idempotency_key:
            self._idem[idempotency_key] = (payload, res)
        return res

    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": self.name(),
            "latency_ms": float(meta.get("latency_ms", 0.0)),
            "attempts": 1,
            "retriable": bool(meta.get("retryable", meta.get("retriable", False))),
        }
