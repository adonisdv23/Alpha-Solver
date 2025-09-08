"""Config loader layering defaults, environment and CLI kwargs."""

from __future__ import annotations

import copy
import os
from typing import Any, Dict

from .defaults import DEFAULT_CONFIG

_ENV_PREFIX = "ALPHA_"


def _coerce(value: str, target: Any) -> Any:
    """Coerce ``value`` to the type of ``target``."""

    if isinstance(target, bool):
        return value.lower() in {"1", "true", "yes"}
    if isinstance(target, tuple):
        return tuple(v.strip() for v in value.split(",") if v.strip())
    return type(target)(value)


def load_config(**kwargs: Any) -> Dict[str, Any]:
    """Return effective configuration with layering ``defaults < env < kwargs``."""

    cfg = copy.deepcopy(DEFAULT_CONFIG)

    # Environment overrides
    for key, default in DEFAULT_CONFIG.items():
        env_key = f"{_ENV_PREFIX}{key.upper()}"
        if env_key in os.environ:
            cfg[key] = _coerce(os.environ[env_key], default)

    # Deterministic mode
    # Timestamp kept deterministic for replay; non-essential for runtime logic.
    cfg["ts"] = 0 if os.getenv("ALPHA_DETERMINISM") == "1" else 0

    # Kwarg overrides
    for key, value in kwargs.items():
        if value is not None:
            cfg[key] = value

    return cfg


__all__ = ["load_config"]
