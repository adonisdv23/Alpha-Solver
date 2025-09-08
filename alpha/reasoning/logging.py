"""Structured JSON logging utilities."""

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

LOGGER = logging.getLogger(__name__)


@dataclass
class JsonlLogger:
    """Tiny logger that appends raw messages to a JSONL file.

    Parameters
    ----------
    path:
        Location of the log file. Each call to :meth:`info` writes a line.
    """

    path: str

    def info(self, message: str) -> None:
        """Append ``message`` to ``path`` with a newline."""
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(f"{message}\n")


def log_event(event: str, *, logger: Optional[logging.Logger] = None, **data: Any) -> None:
    """Log a structured JSON event.

    Parameters
    ----------
    event:
        Name of the event to record.
    logger:
        Optional :class:`logging.Logger` to emit on. Defaults to the module
        logger when ``None``.
    data:
        Additional payload fields stored alongside the event.
    """

    payload = {"event": event, **data, "ts": time.time()}
    (logger or LOGGER).info(json.dumps(payload))


def log_safe_out_decision(
    *,
    route: str,
    conf: float,
    threshold: float,
    reason: str,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Convenience wrapper for SAFE-OUT policy decisions."""
    log_event(
        "safe_out_decision",
        route=route,
        conf=conf,
        threshold=threshold,
        reason=reason,
        logger=logger,
    )
