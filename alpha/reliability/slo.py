"""Utilities for enforcing retry and circuit breaker SLOs."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

RETRY_P95_MAX = 2
BREAKER_OPEN_P95_MAX_MS = 100


def _nearest_rank_p95(values: Sequence[float]) -> float:
    """Return the 95th percentile using the nearest-rank method."""
    numbers = sorted(float(v) for v in values)
    if not numbers:
        return 0.0
    index = max(0, math.ceil(0.95 * len(numbers)) - 1)
    return numbers[index]


def _coerce_metric(value: Any) -> list[float]:
    """Best-effort conversion of ``value`` into a list of floats."""
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        try:
            return [float(v) for v in value]
        except (TypeError, ValueError):  # pragma: no cover - defensive
            return []
    return []


def _extract_metrics(report: dict[str, Any]) -> tuple[list[float], list[float]]:
    retries: list[float] = []
    breaker: list[float] = []

    tests = report.get("tests", [])
    if isinstance(tests, list):
        for entry in tests:
            metadata = entry.get("metadata") if isinstance(entry, dict) else None
            if not isinstance(metadata, dict):
                continue
            if not retries and "retries" in metadata:
                retries = _coerce_metric(metadata.get("retries"))
            if not breaker and "breaker_open_ms" in metadata:
                breaker = _coerce_metric(metadata.get("breaker_open_ms"))

    # Fall back to top-level metadata if present (mirrors pytest-json-report)
    metadata = report.get("metadata")
    if isinstance(metadata, dict):
        if not retries and "retries" in metadata:
            retries = _coerce_metric(metadata.get("retries"))
        if not breaker and "breaker_open_ms" in metadata:
            breaker = _coerce_metric(metadata.get("breaker_open_ms"))

    return retries, breaker


def load_report(path: str | Path) -> dict[str, Any]:
    with Path(path).expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def enforce(path: str | Path) -> dict[str, float]:
    report = load_report(str(path))
    retries, breaker = _extract_metrics(report)
    if not retries:
        raise SystemExit("missing retries metadata")
    if not breaker:
        raise SystemExit("missing breaker_open_ms metadata")

    retry_p95 = _nearest_rank_p95(retries)
    breaker_p95 = _nearest_rank_p95(breaker)
    message = (
        f"[SLO] retry_p95={int(round(retry_p95))} (max<2), "
        f"breaker_open_p95_ms={int(round(breaker_p95))} (max<100)"
    )
    print(message)

    if retry_p95 >= RETRY_P95_MAX or breaker_p95 >= BREAKER_OPEN_P95_MAX_MS:
        raise SystemExit(1)

    return {"retry_p95": retry_p95, "breaker_open_p95_ms": breaker_p95}


def main(argv: Sequence[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: python -m alpha.reliability.slo <report.json>")
        raise SystemExit(2)
    enforce(args[0])


if __name__ == "__main__":
    main()
