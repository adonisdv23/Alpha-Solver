"""Simple in-process alert manager.

The alert manager keeps a rolling window of request latencies and budget
events.  It emits structured alert dictionaries through a callback when:

* the observed p95 latency over the window exceeds ``p95_target_ms``
* a ``budget_over`` event is recorded

The implementation deliberately avoids external services; alerts are delivered
via the provided callback, making it easy for tests to capture and assert on
events.
"""

from __future__ import annotations

import math
import time
from collections import deque
from typing import Callable, Deque, Dict, Iterable, List, Tuple


class AlertManager:
    """Manage latency and budget alerts."""

    def __init__(
        self,
        *,
        p95_target_ms: float = 1000.0,
        window_seconds: float = 60.0,
        callback: Callable[[Dict[str, float]], None] | None = None,
    ) -> None:
        self.p95_target_ms = p95_target_ms
        self.window_seconds = window_seconds
        self.callback = callback or self._default_callback
        self._latencies: Deque[Tuple[float, float]] = deque()
        self._events: List[Dict[str, float]] = []

    # -- internal utilities -------------------------------------------------

    def _default_callback(self, event: Dict[str, float]) -> None:
        self._events.append(event)

    def _emit(self, event: Dict[str, float]) -> None:
        self.callback(event)
        # ensure events are always stored for inspection
        if event not in self._events:
            self._events.append(event)

    def _trim(self, now: float) -> None:
        while self._latencies and now - self._latencies[0][0] > self.window_seconds:
            self._latencies.popleft()

    # -- recording ----------------------------------------------------------

    def record_latency(self, latency_ms: float, *, now: float | None = None) -> None:
        """Record a latency measurement and evaluate alert rules."""

        now = now if now is not None else time.time()
        self._latencies.append((now, latency_ms))
        self._trim(now)
        self._check_latency(now)

    def record_budget_over(self, *, now: float | None = None) -> None:
        """Record that a budget has been exceeded."""

        event = {
            "type": "budget_over",
            "timestamp": now if now is not None else time.time(),
        }
        self._emit(event)

    # -- alert checks -------------------------------------------------------

    def _check_latency(self, now: float) -> None:
        if not self._latencies:
            return
        latencies = [lat for _, lat in self._latencies]
        idx = max(int(math.ceil(0.95 * len(latencies))) - 1, 0)
        p95 = sorted(latencies)[idx]
        if p95 > self.p95_target_ms:
            event = {
                "type": "p95_latency",
                "p95": p95,
                "target": self.p95_target_ms,
                "window": self.window_seconds,
                "timestamp": now,
            }
            self._emit(event)

    # -- public inspection helpers -----------------------------------------

    def get_events(self) -> List[Dict[str, float]]:
        return list(self._events)

    def reset(self) -> None:
        self._latencies.clear()
        self._events.clear()


__all__ = ["AlertManager"]

