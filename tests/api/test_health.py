from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.api.health import HealthChecker, build_health_router


class SlowProbe:
    def __init__(self, delay: float = 0.08) -> None:
        self.delay = delay
        self.calls = 0

    async def __call__(self) -> bool:
        self.calls += 1
        await asyncio.sleep(self.delay)
        return True


def test_health_checker_success_payload() -> None:
    async def scenario() -> None:
        checker = HealthChecker(lambda: True, lambda: "pong", lambda: object())

        payload = await checker.check()

        assert payload["app"] == "ok"
        assert payload["redis"] == "ok"
        assert payload["vectordb"] == "ok"
        assert payload["provider"] == "ok"

        ts = payload["ts"]
        parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        assert parsed.tzinfo is not None
        assert parsed <= datetime.now(timezone.utc)

    asyncio.run(scenario())


def test_health_checker_failure_marks_app_down() -> None:
    async def scenario() -> None:
        def failing_probe() -> bool:
            raise RuntimeError("boom")

        checker = HealthChecker(lambda: True, failing_probe, lambda: True)

        payload = await checker.check()

        assert payload["vectordb"] == "down"
        assert payload["app"] == "down"

    asyncio.run(scenario())


def test_health_checker_warm_cache_under_latency_budget() -> None:
    async def scenario() -> None:
        slow = SlowProbe()
        checker = HealthChecker(slow, lambda: True, lambda: True, cache_ttl=5.0)

        await checker.check()  # warm cache

        start = time.perf_counter()
        payload = await checker.check()
        duration_ms = (time.perf_counter() - start) * 1000

        assert duration_ms < 50.0
        assert payload["redis"] == "ok"
        assert slow.calls == 1

    asyncio.run(scenario())


def test_health_router_smoke() -> None:
    checker = HealthChecker(lambda: True, lambda: True, lambda: True)
    app = FastAPI()
    app.include_router(build_health_router(checker))
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["app"] == "ok"
    assert payload["redis"] == "ok"
    assert "ts" in payload
