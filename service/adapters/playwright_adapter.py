from __future__ import annotations

"""Simulated Playwright adapter with in-memory HTML extraction."""

from time import perf_counter, sleep
from typing import Any, Dict, Tuple
from urllib.parse import urlparse
import re

from .base import AdapterError, IToolAdapter


class PlaywrightAdapter:
    """Tiny in-memory browser emulator.

    It supports a new ``extract`` action used by the hardened tests while still
    retaining the legacy ``get_text``/``click``/``screenshot`` operations so that
    existing tests continue to pass.
    """

    _LATENCY_S = 0.002

    def __init__(self) -> None:
        # Legacy page storage -------------------------------------------------
        self._pages: Dict[str, Dict[str, Any]] = {
            "https://example.com": {"text": "Example Domain", "clicks": 0}
        }
        self._idem: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}

        # HTML snippets for the ``extract`` action ---------------------------
        self._html: Dict[str, str] = {
            "https://example.com": (
                "<html><head>"
                "<meta name='description' content='Example description'></head>"
                "<body><h1>Example Domain</h1>"
                "<p>This domain is for use in illustrative examples in documents."
                " You may use this domain in literature without prior coordination"
                " or asking for permission.</p>"
                "<script>console.log('x')</script>"
                "</body></html>"
            )
        }

    # Protocol methods -------------------------------------------------------
    def name(self) -> str:  # pragma: no cover - trivial
        return "playwright"

    def _run_once(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        """Internal single-attempt execution."""

        if idempotency_key and idempotency_key in self._idem:
            prev_payload, prev_res = self._idem[idempotency_key]
            if prev_payload == payload:
                return prev_res
            raise AdapterError(code="SCHEMA", retryable=False)

        if not isinstance(payload, dict):
            raise AdapterError(code="SCHEMA", retryable=False)

        action = payload.get("action")
        if action == "extract":
            res = self._run_extract(payload, timeout_s=timeout_s)
            return res
        elif action in {"get_text", "click", "screenshot"}:
            res = self._run_legacy(payload, timeout_s=timeout_s)
            if idempotency_key:
                self._idem[idempotency_key] = (payload, res)
            return res
        else:
            raise AdapterError(code="SCHEMA", retryable=False)

    def run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        from .base_adapter import call_adapter

        idempotent = payload.get("action") != "click"
        return call_adapter(
            lambda: self._run_once(payload, idempotency_key=idempotency_key, timeout_s=timeout_s),
            adapter=self.name(),
            idempotent=idempotent,
        )

    # Legacy operations ------------------------------------------------------
    def _run_legacy(self, payload: Dict[str, Any], *, timeout_s: float) -> Dict[str, Any]:
        url = payload.get("url")
        action = payload.get("action")
        if not isinstance(url, str) or action not in {"get_text", "click", "screenshot"}:
            raise AdapterError(code="SCHEMA", retryable=False)

        if timeout_s < self._LATENCY_S:
            raise AdapterError(code="TIMEOUT", retryable=True)

        start = perf_counter()
        sleep(self._LATENCY_S)
        page = self._pages.setdefault(url, {"text": "", "clicks": 0})
        if action == "get_text":
            value: Any = page.get("text", "")
        elif action == "click":
            page["clicks"] = page.get("clicks", 0) + 1
            value = page["clicks"]
        else:  # screenshot
            value = f"screenshot:{url}"
        end = perf_counter()
        meta = {
            "url": url,
            "latency_ms": (end - start) * 1000,
            "retryable": False,
            "attempts": 1,
            "allowlisted": True,
            "sanitized_fields": 0,
        }
        return {"ok": True, "value": value, "meta": meta}

    # Extract operation ------------------------------------------------------
    def _run_extract(self, payload: Dict[str, Any], *, timeout_s: float) -> Dict[str, Any]:
        url = payload.get("url")
        allowlist = payload.get("allowlist")
        selectors = payload.get("selectors")
        if not (
            isinstance(url, str)
            and isinstance(allowlist, list)
            and isinstance(selectors, dict)
        ):
            raise AdapterError(code="SCHEMA", retryable=False)

        domain = urlparse(url).netloc
        allowlisted = domain in allowlist
        if not allowlisted:
            raise AdapterError(code="DOMAIN_NOT_ALLOWED", retryable=False)

        if timeout_s < self._LATENCY_S:
            raise AdapterError(code="TIMEOUT", retryable=True)

        start = perf_counter()
        sleep(self._LATENCY_S)
        html = self._html.get(url, "")
        sanitized_html = self._sanitize_html(html)

        result: Dict[str, str] = {}
        for key, selector in selectors.items():
            if key == "pii_raw":
                continue
            val = self._select(sanitized_html, selector)
            result[key] = self._collapse_ws(val)

        end = perf_counter()
        meta = {
            "latency_ms": (end - start) * 1000,
            "attempts": 1,
            "allowlisted": allowlisted,
            "sanitized_fields": len(result),
        }
        return {"ok": True, "value": result, "meta": meta}

    # Helpers ----------------------------------------------------------------
    def _sanitize_html(self, html: str) -> str:
        """Remove ``script`` and ``style`` blocks."""

        # Avoid regex back-reference quirks by removing ``script`` and ``style``
        # blocks separately.
        html = re.sub(
            r"<script[^>]*>.*?</script>",
            "",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        html = re.sub(
            r"<style[^>]*>.*?</style>",
            "",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        return html

    def _collapse_ws(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def _select(self, html: str, selector: str) -> str:
        if selector == "h1":
            pattern = r"<h1[^>]*>(.*?)</h1>"
        elif selector == "p":
            pattern = r"<p[^>]*>(.*?)</p>"
        elif selector.lower() == "meta[name='description']":
            match = re.search(
                r"<meta[^>]*name=['\"]description['\"][^>]*content=['\"](.*?)['\"][^>]*>",
                html,
                flags=re.IGNORECASE,
            )
            return match.group(1) if match else ""
        else:
            tag = re.escape(selector)
            pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"

        m = re.search(pattern, html, flags=re.DOTALL | re.IGNORECASE)
        return m.group(1) if m else ""

    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": self.name(),
            "latency_ms": float(meta.get("latency_ms", 0.0)),
            "attempts": int(meta.get("attempts", 1)),
            "allowlisted": bool(meta.get("allowlisted", False)),
            "sanitized_fields": int(meta.get("sanitized_fields", 0)),
            "retriable": bool(meta.get("retryable", meta.get("retriable", False))),
        }

