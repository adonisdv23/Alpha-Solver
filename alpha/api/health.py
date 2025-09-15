from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

__all__ = ["get_health"]


def get_health(
    redis_client: Optional[Any] = None,
    *,
    vectordb_ok: bool | None = None,
    provider_ok: bool | None = None,
) -> Dict[str, str]:
    """Return application and dependency health information.

    The function avoids network calls unless a ``redis_client`` is provided.
    ``vectordb_ok`` and ``provider_ok`` flags allow callers to supply cached
    health information. When ``None`` they default to ``down``.
    """

    def _status(flag: bool | None) -> str:
        return "ok" if flag else "down"

    redis_status = "down"
    if redis_client is not None:
        try:
            if redis_client.ping():
                redis_status = "ok"
        except Exception:
            redis_status = "down"

    payload: Dict[str, str] = {
        "app": "ok",
        "redis": redis_status,
        "vectordb": _status(vectordb_ok),
        "provider": _status(provider_ok),
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    return payload


if __name__ == "__main__":  # pragma: no cover - manual debugging helper
    import json

    print(json.dumps(get_health(), indent=2))
