from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

__all__ = ["get_health", "router"]


def get_health(
    redis_client: Optional[Any] = None,
    *,
    vectordb_ok: bool | None = None,
    provider_ok: bool | None = None,
) -> Dict[str, str]:
    """Return application and dependency health information."""

    def _status(flag: bool | None) -> str:
        return "ok" if flag else "down"

    redis_status = "down"
    if redis_client is not None:
        try:
            if redis_client.ping():
                redis_status = "ok"
        except Exception:
            redis_status = "down"

    return {
        "app": "ok",
        "redis": redis_status,
        "vectordb": _status(vectordb_ok),
        "provider": _status(provider_ok),
        "ts": datetime.now(timezone.utc).isoformat(),
    }


# Optional FastAPI router for service integration
try:  # pragma: no cover - only exercised in integration tests
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/health")
    def health_endpoint() -> Dict[str, str]:
        return get_health()
except Exception:  # pragma: no cover - fastapi not installed
    router = None


if __name__ == "__main__":  # pragma: no cover - manual debugging helper
    import json

    print(json.dumps(get_health(), indent=2))
