import json
import logging
import time
from typing import Any

LOGGER = logging.getLogger(__name__)


def log_event(event: str, **data: Any) -> None:
    """Log a structured JSON event."""
    payload = {"event": event, **data, "ts": time.time()}
    LOGGER.info(json.dumps(payload))
