from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


class AlphaClient:
    """Minimal HTTP client for the Alpha Solver API."""

    def __init__(self, api_url: str, api_key: str) -> None:
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key

    def solve(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        strategy: Optional[str] = None,
        timeout: float = 10.0,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"query": prompt}
        if context:
            payload["context"] = context
        if strategy:
            payload["strategy"] = strategy
        data = json.dumps(payload).encode("utf-8")
        url = f"{self.api_url}/v1/solve"
        headers = {"Content-Type": "application/json", "X-API-Key": self.api_key}
        backoff = 0.5
        for attempt in range(3):
            req = urllib.request.Request(url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read().decode("utf-8")
                    result = json.loads(body)
                    req_id = resp.headers.get("X-Request-ID")
                    if req_id:
                        result["request_id"] = req_id
                    return result
            except urllib.error.HTTPError as e:  # pragma: no cover - network errors
                if e.code in {429, 500, 502, 503, 504} and attempt < 2:
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 2.0)
                    continue
                raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8')}")
            except urllib.error.URLError as e:  # pragma: no cover - network errors
                if attempt < 2:
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 2.0)
                    continue
                raise RuntimeError(f"request failed: {e.reason}")
        raise RuntimeError("max retries exceeded")


__all__ = ["AlphaClient"]
