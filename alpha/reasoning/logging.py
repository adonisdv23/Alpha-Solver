import json
import logging
import time
from typing import Any

LOGGER = logging.getLogger(__name__)


def log_event(event: str, **data: Any) -> None:
    """Log a structured JSON event."""
    payload = {"event": event, **data, "ts": time.time()}
    LOGGER.info(json.dumps(payload))


def log_safe_out_decision(*, route: str, conf: float, threshold: float, reason: str) -> None:
    """Convenience wrapper for SAFE-OUT policy decisions."""
    log_event("safe_out_decision", route=route, conf=conf, threshold=threshold, reason=reason)


def log_safe_out_phase(*, phase: str, route: str, conf: float, threshold: float) -> None:
    """Log a SAFE-OUT state machine phase transition."""
    log_event("safe_out_phase", phase=phase, route=route, conf=conf, threshold=threshold)
