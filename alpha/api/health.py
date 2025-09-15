"""Health check utilities for the Alpha Solver HTTP surface."""

from __future__ import annotations

import asyncio
import inspect
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Awaitable, Callable, Dict, Mapping

from typing_extensions import TypedDict

from fastapi import APIRouter


class HealthPayload(TypedDict):
    """JSON payload returned by the ``/health`` endpoint."""

    app: str
    redis: str
    vectordb: str
    provider: str
    ts: str


Probe = Callable[[], Awaitable[object] | object]
Clock = Callable[[], float]


def _iso_timestamp() -> str:
    """Return the current UTC timestamp formatted for JSON payloads."""

    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


async def _run_probe(probe: Probe) -> str:
    """Execute a dependency probe and normalise its status.

    A probe is expected to return a truthy value on success. Any exception raised
    by the probe is treated as a failure and results in a ``"down"`` status.
    """

    try:
        result = probe()
        if inspect.isawaitable(result):
            result = await result
    except Exception:
        return "down"

    if result is None:
        return "ok"
    try:
        return "ok" if bool(result) else "down"
    except Exception:
        return "ok"


@dataclass
class HealthChecker:
    """Aggregate dependency probes into the health payload.

    The checker executes Redis, Vector DB and model provider probes and caches the
    resulting status for ``cache_ttl`` seconds. Caching keeps subsequent endpoint
    calls comfortably under the 50ms latency budget after the first (warm cache)
    request.
    """

    redis_probe: Probe
    vectordb_probe: Probe
    provider_probe: Probe
    cache_ttl: float = 5.0
    clock: Clock = time.monotonic
    _cache: Mapping[str, str] | None = field(default=None, init=False)
    _cached_at: float | None = field(default=None, init=False)
    _lock: asyncio.Lock | None = field(default=None, init=False, repr=False)

    async def check(self) -> HealthPayload:
        """Return the aggregated health payload, using the warm cache when valid."""

        cached = self._cached_status()
        if cached:
            return self._compose_payload(cached)

        lock = self._ensure_lock()
        async with lock:
            cached = self._cached_status()
            if cached:
                return self._compose_payload(cached)

            statuses = await self._evaluate()
            self._cache = statuses
            self._cached_at = self.clock()

        return self._compose_payload(statuses)

    def invalidate(self) -> None:
        """Clear the cached health status, forcing fresh probes on next call."""

        self._cache = None
        self._cached_at = None

    def _cached_status(self) -> Mapping[str, str] | None:
        if self._cache is None or self._cached_at is None:
            return None
        if self.clock() - self._cached_at >= self.cache_ttl:
            return None
        return self._cache

    def _ensure_lock(self) -> asyncio.Lock:
        lock = self._lock
        if lock is None:
            lock = asyncio.Lock()
            self._lock = lock
        return lock

    async def _evaluate(self) -> Dict[str, str]:
        redis_status, vectordb_status, provider_status = await asyncio.gather(
            _run_probe(self.redis_probe),
            _run_probe(self.vectordb_probe),
            _run_probe(self.provider_probe),
        )
        return {
            "redis": redis_status,
            "vectordb": vectordb_status,
            "provider": provider_status,
        }

    def _compose_payload(self, statuses: Mapping[str, str]) -> HealthPayload:
        return {
            "app": "ok" if all(status == "ok" for status in statuses.values()) else "down",
            "redis": statuses.get("redis", "down"),
            "vectordb": statuses.get("vectordb", "down"),
            "provider": statuses.get("provider", "down"),
            "ts": _iso_timestamp(),
        }


def build_health_router(checker: HealthChecker) -> APIRouter:
    """Return a FastAPI router exposing ``/health`` backed by ``checker``."""

    router = APIRouter()

    @router.get("/health", name="health", tags=["health"])
    async def health_endpoint() -> HealthPayload:  # pragma: no cover - exercised via router
        return await checker.check()

    return router


__all__ = ["HealthChecker", "HealthPayload", "build_health_router"]
