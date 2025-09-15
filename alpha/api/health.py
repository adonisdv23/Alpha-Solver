from __future__ import annotations

import asyncio
import time
from typing import Dict

from fastapi import APIRouter, FastAPI

try:  # pragma: no cover - optional dependency
    import redis.asyncio as redis  # type: ignore
except Exception:  # pragma: no cover - best effort
    redis = None  # type: ignore

router = APIRouter()
app = FastAPI()


async def _check_redis() -> str:
    """Ping local Redis instance and return ``ok`` or ``down``.

    The check uses a tiny connection timeout so that failures return quickly
    (<50ms) and do not block the health endpoint.
    """
    if redis is None:
        return "down"
    try:
        client = redis.from_url(
            "redis://localhost", socket_connect_timeout=0.05, socket_timeout=0.05
        )
        await client.ping()
        return "ok"
    except Exception:
        return "down"


def _check_vectordb() -> str:
    """Placeholder vector DB check.

    In a production deployment this function would ping the configured vector
    database. For the open-source tree it simply reports ``ok`` so that the
    structure of the response is exercised without requiring heavy
    dependencies.
    """
    return "ok"


async def _check_provider() -> str:
    """Verify that the default provider client can be imported.

    The function avoids external network calls to keep the endpoint fast and
    deterministic in tests. Import errors are treated as a failure.
    """
    try:
        import httpx  # noqa: F401

        return "ok"
    except Exception:
        return "down"


@router.get("/health")
async def health() -> Dict[str, object]:
    """Return application and dependency health information."""
    redis_status, provider_status = await asyncio.gather(
        _check_redis(), _check_provider()
    )
    payload: Dict[str, object] = {
        "app": "ok",
        "redis": redis_status,
        "vectordb": _check_vectordb(),
        "provider": provider_status,
        "ts": time.time(),
    }
    return payload


app.include_router(router)

__all__ = ["app", "health", "_check_redis", "_check_provider", "_check_vectordb"]
