import json
import logging
import time
from typing import Any

from alpha.core.replay import ReplayHarness

LOGGER = logging.getLogger(__name__)

CURRENT_REPLAY_HARNESS: ReplayHarness | None = None
SESSION_ID = "session-0"


def set_replay_harness(harness: ReplayHarness | None) -> None:
    """Register a global replay harness for event capture."""
    global CURRENT_REPLAY_HARNESS
    CURRENT_REPLAY_HARNESS = harness


def set_session_id(session_id: str) -> None:
    global SESSION_ID
    SESSION_ID = session_id


def log_event(event: str, **data: Any) -> None:
    """Log a structured JSON event compatible with telemetry schema."""
    payload = {
        "session_id": SESSION_ID,
        "event": event,
        "timestamp": time.time(),
        "version": "1.0",
        "data": data,
    }
    LOGGER.info(json.dumps(payload))
    if CURRENT_REPLAY_HARNESS is not None:
        CURRENT_REPLAY_HARNESS.record(payload)


def log_safe_out_decision(*, route: str, conf: float, threshold: float, reason: str) -> None:
    """Convenience wrapper for SAFE-OUT policy decisions."""
    log_event("safe_out_decision", route=route, conf=conf, threshold=threshold, reason=reason)
