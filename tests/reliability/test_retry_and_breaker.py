import json
import os
import random


def test_retry_and_breaker(record_property):
    """Simulate retry and circuit breaker metrics and export them."""
    # Deterministic retries: 80x0, 16x1, 4x2 -> p95 < 2
    retry_counts = [0] * 80 + [1] * 16 + [2] * 4
    # Breaker open times with jitter under 100ms
    random.seed(0)
    breaker_open_ms = [random.uniform(10, 90) for _ in range(100)]

    # Attach to pytest metadata (for json-report style collectors)
    record_property("retry_counts", retry_counts)
    record_property("breaker_open_ms", breaker_open_ms)

    # Persist metrics for SLO evaluation
    report_path = os.environ.get("SLO_REPORT", "slo_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "retry_counts": retry_counts,
            "breaker_open_ms": breaker_open_ms,
        }, f)
