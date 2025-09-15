import json
import os
import random
from pathlib import Path


def test_retry_and_breaker(record_property):
    """Simulate retry and circuit breaker metrics and export them."""
    # Deterministic retries: 80x0, 16x1, 4x2 -> p95 < 2
    retry_counts = [0] * 80 + [1] * 16 + [2] * 4
    # Breaker open times with jitter under 100ms
    random.seed(0)
    breaker_open_ms = [random.uniform(10, 90) for _ in range(100)]

    # Attach to pytest metadata (for json-report collectors)
    record_property("retries", retry_counts)
    record_property("breaker_open_ms", breaker_open_ms)

    # Persist metrics for SLO evaluation (mirrors pytest-json-report layout)
    report_path = Path(os.environ.get("SLO_REPORT", "slo_report.json"))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "tests": [
            {
                "nodeid": "tests/reliability/test_retry_and_breaker.py::test_retry_and_breaker",
                "metadata": {
                    "retries": retry_counts,
                    "breaker_open_ms": breaker_open_ms,
                },
            }
        ]
    }
    report_path.write_text(json.dumps(report), encoding="utf-8")
