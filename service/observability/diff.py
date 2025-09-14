from __future__ import annotations

"""Helpers to produce unified diffs between observability logs."""

import difflib
import json
from typing import Any, Dict, Iterable, List, Optional

from .replay import ReplayHarness

__all__ = ["diff_events", "diff_logs"]


# ---------------------------------------------------------------------------
def _events_to_lines(events: Iterable[Dict[str, Any]]) -> List[str]:
    """Normalise event dictionaries into stable JSON lines."""
    lines: List[str] = []
    for event in events:
        lines.append(json.dumps(event, sort_keys=True, separators=(",", ":")))
    return lines


# ---------------------------------------------------------------------------
def diff_events(
    events_a: Iterable[Dict[str, Any]],
    events_b: Iterable[Dict[str, Any]],
) -> str:
    """Return a unified diff between two event collections."""

    a_lines = _events_to_lines(events_a)
    b_lines = _events_to_lines(events_b)
    diff = difflib.unified_diff(a_lines, b_lines, fromfile="a", tofile="b", lineterm="")
    return "\n".join(diff)


# ---------------------------------------------------------------------------
def diff_logs(path_a: str, path_b: str, name: Optional[str] = None) -> str:
    """Diff two JSONL log files on disk."""

    harness_a = ReplayHarness(path_a)
    harness_b = ReplayHarness(path_b)
    return diff_events(harness_a.iter_events(name), harness_b.iter_events(name))
