"""Determinism harness for detecting non deterministic behavior.

This module provides a small utility used in tests to run a callable
multiple times with the same inputs and report if the outputs "flap"
(i.e. vary across runs).  It can also replay RES-07 events which are
already materialised as dictionaries.

The harness is intentionally lightweight and does not depend on the rest
of the Alpha solver stack.  It is meant for unit tests and small scripts
so performance and determinism are prioritised over features.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Any, Dict, List
import math
import random
import time

from .report import tiebreak_diff


# ---------------------------------------------------------------------------
# helper functions
# ---------------------------------------------------------------------------

def _float_digits(tol: float) -> int:
    """Return the number of decimal digits necessary for ``tol``.

    ``float_tol`` is expressed as an absolute tolerance (e.g. ``1e-6``) and
    we convert that to a number of digits to be used with ``round``.  The
    conversion is deterministic and avoids dependencies on ``math.isclose``
    which uses relative tolerance.
    """

    if tol <= 0:
        return 6
    return max(0, int(abs(math.log10(tol))))


def normalize(o: Dict[str, Any], *, float_tol: float, compare_keys: Iterable[str]) -> Dict[str, Any]:
    """Normalise an output dictionary for comparison.

    Only ``compare_keys`` are kept.  Floating point values are rounded so
    that tiny jitter does not trigger false positives.  Keys that look like
    secrets or raw PII are dropped regardless of ``compare_keys``.
    """

    digits = _float_digits(float_tol)
    out: Dict[str, Any] = {}
    for key in compare_keys:
        if key not in o:
            continue
        if key == "pii_raw" or key.endswith("_token") or key.endswith("_secret"):
            continue
        val = o[key]
        if isinstance(val, float):
            val = round(val, digits)
        out[key] = val
    return out


def inject_factor_noise(value: Any, pct: int) -> Any:
    """Inject multiplicative noise into numeric ``value``.

    This helper is only used in tests to simulate non semantic noise.  For
    non numeric values the ``value`` is returned unchanged.
    """

    if isinstance(value, (int, float)):
        factor = 1 + random.uniform(-pct, pct) / 100.0
        return value * factor
    return value


# ---------------------------------------------------------------------------
# Harness implementation
# ---------------------------------------------------------------------------


@dataclass
class DeterminismHarness:
    """Utility to run callables or replay events multiple times.

    Parameters mirror the configuration file ``config/determinism.yaml``.
    ``compare_keys`` defaults to a set of RES-07 aligned keys.
    """

    runs: int = 100
    factor_noise_pct: int = 3
    float_tol: float = 1e-6
    compare_keys: List[str] | None = None
    fail_on_flap: bool = True

    def __post_init__(self) -> None:
        if self.compare_keys is None:
            self.compare_keys = [
                "decision",
                "confidence",
                "budget_verdict",
                "score",
                "tool",
                "sandbox_decision",
            ]

    # ------------------------------------------------------------------
    def run_callable(self, fn: Callable[..., Dict[str, Any]], *, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run ``fn`` repeatedly for each input and collect stability stats.

        ``inputs`` is a list of dictionaries.  Each dictionary may contain an
        ``id`` key used for reporting; the remaining keys are passed to ``fn``
        as keyword arguments.
        """

        cases: List[Dict[str, Any]] = []
        flaps = 0
        for idx, raw in enumerate(inputs):
            case_id = raw.get("id", idx)
            kwargs = {k: v for k, v in raw.items() if k != "id"}
            outputs: List[Dict[str, Any]] = []
            timings: List[float] = []
            for _ in range(self.runs):
                start = time.monotonic()
                out = fn(**kwargs)
                timings.append(time.monotonic() - start)
                outputs.append(normalize(out, float_tol=self.float_tol, compare_keys=self.compare_keys))
            first = outputs[0]
            unique: List[Dict[str, Any]] = []
            for o in outputs:
                if o not in unique:
                    unique.append(o)
            stable = len(unique) == 1
            if not stable:
                flaps += 1
            diffs: List[str] = []
            if not stable:
                for variant in unique[1:]:
                    diffs.extend(tiebreak_diff(first, variant, keys=self.compare_keys))
            cases.append(
                {
                    "id": case_id,
                    "stable": stable,
                    "variants": len(unique),
                    "first": first,
                    "diffs": diffs,
                    "timings": timings,
                }
            )
        return {"total": len(cases), "flaps": flaps, "cases": cases}

    # ------------------------------------------------------------------
    def run_replay(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse RES-07 shaped replay ``events``.

        Events are dictionaries which include an ``id`` key along with output
        fields.  They may contain multiple entries for the same ``id`` which
        represent repeated runs.  The method normalises the fields and detects
        flaps similar to :meth:`run_callable`.
        """

        grouped: Dict[Any, List[Dict[str, Any]]] = {}
        for e in events:
            case_id = e.get("id")
            grouped.setdefault(case_id, []).append(e)

        cases: List[Dict[str, Any]] = []
        flaps = 0
        for case_id, group in grouped.items():
            outputs = [normalize(ev, float_tol=self.float_tol, compare_keys=self.compare_keys) for ev in group]
            first = outputs[0]
            unique: List[Dict[str, Any]] = []
            for o in outputs:
                if o not in unique:
                    unique.append(o)
            stable = len(unique) == 1
            if not stable:
                flaps += 1
            diffs: List[str] = []
            if not stable:
                for variant in unique[1:]:
                    diffs.extend(tiebreak_diff(first, variant, keys=self.compare_keys))
            cases.append(
                {
                    "id": case_id,
                    "stable": stable,
                    "variants": len(unique),
                    "first": first,
                    "diffs": diffs,
                    "timings": [],
                }
            )
        return {"total": len(cases), "flaps": flaps, "cases": cases}

    # ------------------------------------------------------------------
    def is_stable(self, case_summary: Dict[str, Any]) -> bool:
        """Return ``True`` if a case is stable (no flaps)."""

        if "stable" in case_summary:
            return bool(case_summary["stable"])
        return case_summary.get("variants", 1) <= 1
