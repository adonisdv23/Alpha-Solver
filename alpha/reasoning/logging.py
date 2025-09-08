"""Structured logging helpers for reasoning components.

This module provides a tiny JSON logger with deterministic timestamp handling and
per-run identifiers.  All events emitted here are additive; existing schemas are
unchanged.  When the environment variable ``ALPHA_DETERMINISM`` is set to ``1``
timestamps advance deterministically from ``0``.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any, Dict

LOGGER = logging.getLogger(__name__)


_DETERMINISTIC = os.getenv("ALPHA_DETERMINISM") == "1"
_RUN_ID = os.environ.get("ALPHA_RUN_ID", uuid.uuid4().hex)
_START_TS = 0.0 if _DETERMINISTIC else time.time()
_TS_COUNTER = 0


def _now() -> float:
    """Return a monotonically increasing timestamp."""

    global _TS_COUNTER
    if _DETERMINISTIC:
        ts = _START_TS + _TS_COUNTER
        _TS_COUNTER += 1
        return ts
    return time.time()


def get_run_id() -> str:
    """Expose the current run identifier."""

    return _RUN_ID


def log_event(event: str, *, layer: str | None = None, **data: Any) -> None:
    """Log a structured JSON event.

    Parameters
    ----------
    event:
        Event name.
    layer:
        Optional subsystem emitting the event (e.g. ``"tot"`` or ``"router"``).
    **data:
        Additional payload fields.
    """

    payload: Dict[str, Any] = {
        "event": event,
        **data,
        "ts": _now(),
        "run_id": _RUN_ID,
    }
    if layer is not None:
        payload["layer"] = layer
    LOGGER.info(json.dumps(payload, sort_keys=True))


def log_safe_out_decision(*, route: str, conf: float, threshold: float, reason: str) -> None:
    """Convenience wrapper for SAFE-OUT policy decisions."""

    log_event(
        "safe_out_decision",
        layer="safe_out",
        route=route,
        conf=conf,
        threshold=threshold,
        reason=reason,
    )


def log_safe_out_phase(*, phase: str, route: str, conf: float, threshold: float) -> None:
    """Log a SAFE-OUT state machine phase transition."""

    log_event(
        "safe_out_phase",
        layer="safe_out",
        phase=phase,
        route=route,
        conf=conf,
        threshold=threshold,
    )


def emit_run_summary(*, counts: Dict[str, int], final_route: str, final_confidence: float) -> None:
    """Emit a run-level summary event.

    Parameters
    ----------
    counts:
        Simple counters for the run (e.g. explored nodes).
    final_route:
        Final policy route taken.
    final_confidence:
        Confidence associated with the final answer.
    """

    log_event(
        "run_summary",
        layer="run",
        counts=counts,
        final_route=final_route,
        final_confidence=final_confidence,
    )


__all__ = [
    "emit_run_summary",
    "get_run_id",
    "log_event",
    "log_safe_out_decision",
    "log_safe_out_phase",
]
