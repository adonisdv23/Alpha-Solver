"""Routes powering the dashboard one-click demo run page."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_RUN_TEMPLATE_PATH = _TEMPLATES_DIR / "run.html"
_TEMPLATE_CACHE: Optional[str] = None


@dataclass
class DemoRunResult:
    """Structured payload returned by the mock demo broker."""

    result: str
    latency_ms: float
    cache_hit: bool

    def to_dict(self) -> Dict[str, object]:
        return {
            "result": self.result,
            "latency_ms": float(self.latency_ms),
            "cache_hit": self.cache_hit,
        }


class _MockDemoBroker:
    """A lightweight broker that simulates executing a canned request."""

    _CACHE_KEY = "demo"

    def __init__(self) -> None:
        self._cache: Dict[str, str] = {}
        self._lock = threading.Lock()

    def run(self) -> DemoRunResult:
        with self._lock:
            cached_result = self._cache.get(self._CACHE_KEY)

        if cached_result is not None:
            latency_ms = _simulate_latency(cache_hit=True)
            return DemoRunResult(result=cached_result, latency_ms=latency_ms, cache_hit=True)

        latency_ms = _simulate_latency(cache_hit=False)
        result_text = _render_demo_result()
        with self._lock:
            self._cache[self._CACHE_KEY] = result_text
        return DemoRunResult(result=result_text, latency_ms=latency_ms, cache_hit=False)

    def reset(self) -> None:
        with self._lock:
            self._cache.clear()


_BROKER = _MockDemoBroker()


def _simulate_latency(cache_hit: bool) -> float:
    """Return a deterministic latency budget in milliseconds."""

    base_seconds = 0.11 if not cache_hit else 0.008
    time.sleep(base_seconds)
    return round(base_seconds * 1000.0, 2)


def _render_demo_result() -> str:
    """Produce the canned result snippet displayed in the UI."""

    return (
        "Alpha Solver demo completed successfully.\n"
        "\n"
        "Highlights:\n"
        "- Validated retrieval pipeline across two corpora.\n"
        "- Generated actionable next steps for the research team.\n"
        "- Confirmed observability hooks are emitting latency metrics."
    )


def _load_template() -> str:
    global _TEMPLATE_CACHE
    if _TEMPLATE_CACHE is None:
        _TEMPLATE_CACHE = _RUN_TEMPLATE_PATH.read_text(encoding="utf-8")
    return _TEMPLATE_CACHE


def reset_state() -> None:
    """Reset broker state for hermetic tests."""

    _BROKER.reset()


@router.get("/run", response_class=HTMLResponse)
async def run_page(request: Request) -> HTMLResponse:
    """Serve the dashboard page with the demo run button."""

    _ = request  # FastAPI expects the request argument even for static templates.
    return HTMLResponse(content=_load_template())


@router.post("/run")
async def trigger_demo(_: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    """Execute the canned demo request via the mock broker."""

    result = _BROKER.run()
    return result.to_dict()
