import json
import logging
import time
from typing import Any, Literal, Optional

LOGGER = logging.getLogger(__name__)


def log_event(event: str, **data: Any) -> None:
    """Log a structured JSON event."""
    payload = {"event": event, **data, "ts": time.time()}
    LOGGER.info(json.dumps(payload))


Phase = Literal["init", "assess", "fallback", "finalize"]


def log_safe_out_phase(
    *, phase: Phase, route: Optional[str] = None, conf: Optional[float] = None, threshold: Optional[float] = None
) -> None:
    """Log a SAFE-OUT state-machine phase transition."""
    log_event("safe_out_phase", phase=phase, route=route, conf=conf, threshold=threshold)


def log_safe_out_decision(*, route: str, conf: float, threshold: float, reason: str) -> None:
    """Convenience wrapper for SAFE-OUT policy decisions."""
    log_event("safe_out_decision", route=route, conf=conf, threshold=threshold, reason=reason)
