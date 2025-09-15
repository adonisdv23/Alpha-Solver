"""Utilities for enforcing retry and circuit breaker SLOs."""
import json
import math
import sys
from typing import Sequence

RETRY_P95_THRESHOLD = 2
BREAKER_P95_THRESHOLD_MS = 100


def p95(values: Sequence[float]) -> float:
    """Return the 95th percentile of ``values``.

    Uses the nearest-rank method which matches common SLO calculations.
    Returns 0.0 for empty input.
    """
    vals = sorted(values)
    if not vals:
        return 0.0
    index = math.ceil(0.95 * len(vals)) - 1
    return float(vals[index])


def load_report(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def enforce(path: str) -> dict:
    """Validate the metrics in ``path`` against SLO thresholds.

    Returns a dictionary with computed p95 statistics.
    Raises ``SystemExit`` with code 1 if the SLO is violated or jitter is absent.
    """
    data = load_report(path)
    retries = data.get("retry_counts", [])
    breaker = data.get("breaker_open_ms", [])

    retry_p95 = p95(retries)
    breaker_p95 = p95(breaker)

    if len(set(retries)) <= 1:
        raise SystemExit("retry jitter not enforced")
    if len(set(breaker)) <= 1:
        raise SystemExit("breaker jitter not enforced")
    if retry_p95 >= RETRY_P95_THRESHOLD:
        raise SystemExit(f"retry_p95 {retry_p95} >= {RETRY_P95_THRESHOLD}")
    if breaker_p95 >= BREAKER_P95_THRESHOLD_MS:
        raise SystemExit(
            f"breaker_open_p95_ms {breaker_p95} >= {BREAKER_P95_THRESHOLD_MS}"
        )

    return {"retry_p95": retry_p95, "breaker_open_p95_ms": breaker_p95}


def main(argv: Sequence[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("Usage: slo.py <report.json>")
        raise SystemExit(2)
    stats = enforce(argv[0])
    print(
        f"retry_p95={stats['retry_p95']:.2f} "
        f"breaker_open_p95_ms={stats['breaker_open_p95_ms']:.2f}"
    )


if __name__ == "__main__":
    main()
