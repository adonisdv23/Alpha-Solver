"""Reporting utilities for the determinism harness."""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List
import math


def tiebreak_diff(a: Dict[str, Any], b: Dict[str, Any], *, keys: Iterable[str]) -> List[str]:
    """Return deterministic diff lines between ``a`` and ``b``.

    Each entry is of the form ``"key: a_val vs b_val"``.  ``keys`` controls
    the order of the diff and typically comes from the harness
    configuration.
    """

    lines: List[str] = []
    for key in sorted(keys):
        va = a.get(key)
        vb = b.get(key)
        if va != vb:
            lines.append(f"{key}: {va} vs {vb}")
    return lines


def _p95(values: List[float]) -> float | None:
    if not values:
        return None
    values = sorted(values)
    idx = max(0, int(math.ceil(0.95 * len(values))) - 1)
    return values[idx]


def summarize(result: Dict[str, Any]) -> Dict[str, Any]:
    """Summarise harness ``result``.

    The returned dictionary includes totals, flap rate, optional p95 timings
    and a breakdown of the most common offending keys.
    """

    total = result.get("total", 0)
    flaps = result.get("flaps", 0)
    summary: Dict[str, Any] = {
        "total": total,
        "flaps": flaps,
        "flap_rate": (flaps / total) if total else 0.0,
    }

    # timings
    timings: List[float] = []
    for case in result.get("cases", []):
        timings.extend(case.get("timings", []))
    p95 = _p95(timings)
    if p95 is not None:
        summary["p95_ms"] = p95 * 1000

    # offending keys
    counter: Counter[str] = Counter()
    for case in result.get("cases", []):
        for diff in case.get("diffs", []):
            key = diff.split(":", 1)[0]
            counter[key] += 1
    summary["top_keys"] = dict(counter.most_common())
    return summary
