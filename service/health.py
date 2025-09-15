from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict

from fastapi import FastAPI

# Record application start for uptime calculations
START_TIME = time.time()

# Pre-import the model provider so that health checks remain fast even on the
# first call. Import errors are captured in ``_MODEL_PROVIDER_AVAILABLE``.
try:  # pragma: no cover - import guard
    import alpha.adapters.base as _adapter_base  # type: ignore  # noqa: F401

    _MODEL_PROVIDER_AVAILABLE = True
except Exception:  # pragma: no cover - best effort
    _MODEL_PROVIDER_AVAILABLE = False


def _registry_path() -> Path:
    """Return path to the tools registry file.

    The registry is considered a critical dependency for the service. The check
    simply verifies that the file exists and is valid JSON. Any exception should
    be treated as a failure.
    """
    return Path(__file__).resolve().parents[1] / "registries" / "tools.json"


async def probe_adapter_registry() -> bool:
    """Probe the adapter registry.

    Returns ``True`` when the registry file can be loaded, ``False`` otherwise.
    The implementation avoids network access and completes quickly (<100ms).
    """
    try:
        with _registry_path().open("r", encoding="utf-8") as fh:
            json.load(fh)
        return True
    except Exception:
        return False


async def probe_model_provider() -> bool:
    """Probe the default model provider.

    The probe simply reports the result of the import attempt performed at module
    import time. This keeps the endpoint fast while still detecting missing
    dependencies.
    """
    return _MODEL_PROVIDER_AVAILABLE


async def healthcheck(app: FastAPI) -> Dict[str, object]:
    """Return the aggregated health payload for the service."""
    deps = {
        "adapter_registry": await probe_adapter_registry(),
        "model_provider": await probe_model_provider(),
    }
    status = "ok" if all(deps.values()) else "error"
    started = getattr(app.state, "start_time", START_TIME)
    payload: Dict[str, object] = {
        "status": status,
        "version": getattr(app.state.config, "version", "unknown"),
        "uptime_s": round(time.time() - started, 3),
        "deps": deps,
    }
    return payload


__all__ = [
    "healthcheck",
    "probe_adapter_registry",
    "probe_model_provider",
]
