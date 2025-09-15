from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

import pytest
from prometheus_client import CollectorRegistry

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.finops.budget import BudgetExceeded, BudgetManager


def test_budget_counters_are_scoped() -> None:
    manager = BudgetManager()
    manager.register_budget("tenant-a", "project-1", soft_limit_cents=120, hard_limit_cents=400)
    manager.register_budget("tenant-b", "project-2", soft_limit_cents=300, hard_limit_cents=900)

    first = manager.record_tokens("tenant-a", "project-1", provider="openai:gpt-4", tokens=10)
    assert first["total_spend_cents"] == manager.calculate_cost_cents("openai:gpt-4", 10)

    second = manager.record_tokens("tenant-a", "project-1", provider="openai:gpt-4", tokens=5)
    other = manager.record_tokens("tenant-b", "project-2", provider="openai:gpt-3.5", tokens=20)

    usage_a = manager.get_usage("tenant-a", "project-1")
    usage_b = manager.get_usage("tenant-b", "project-2")

    assert usage_a["spend_cents"] == second["total_spend_cents"]
    assert usage_b["spend_cents"] == other["total_spend_cents"]
    assert usage_a["events"] == 2
    assert usage_b["events"] == 1

    snapshot = manager.snapshot()
    assert snapshot[("tenant-a", "project-1")]["spend_cents"] != snapshot[("tenant-b", "project-2")]["spend_cents"]


def test_soft_cap_emits_warning_once(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    manager = BudgetManager()
    manager.register_budget("tenant", "project", soft_limit_cents=50, hard_limit_cents=200)

    manager.record_tokens("tenant", "project", provider="openai:gpt-3.5", tokens=50)

    caplog.clear()
    manager.record_tokens("tenant", "project", provider="openai:gpt-4", tokens=80)

    warnings = [record for record in caplog.records if record.levelno == logging.WARNING]
    assert warnings, "Expected a warning once the soft cap is crossed"
    assert "soft cap" in warnings[0].message.lower()
    assert manager.get_usage("tenant", "project")["soft_alert_triggered"] is True

    caplog.clear()
    manager.record_tokens("tenant", "project", provider="openai:gpt-3.5", tokens=5)
    assert caplog.records == []


def test_hard_cap_blocks_and_preserves_state() -> None:
    manager = BudgetManager()
    manager.register_budget("tenant", "project", soft_limit_cents=40, hard_limit_cents=60)

    manager.record_cost("tenant", "project", 40, provider="manual")

    with pytest.raises(BudgetExceeded) as excinfo:
        manager.record_cost("tenant", "project", 30, provider="manual")

    usage = manager.get_usage("tenant", "project")
    assert usage["spend_cents"] == 40
    assert usage["events"] == 1

    err = excinfo.value
    assert err.attempted_spend_cents == 70
    assert err.hard_limit_cents == 60


def test_metric_records_spend_values() -> None:
    registry = CollectorRegistry()
    manager = BudgetManager(registry=registry)
    manager.register_budget("tenant", "project", soft_limit_cents=100, hard_limit_cents=500)

    result = manager.record_tokens("tenant", "project", provider="openai:gpt-4o", tokens=20)

    metric_value = registry.get_sample_value(
        "budget_spend_cents_total",
        labels={"tenant": "tenant", "project": "project", "provider": "openai:gpt-4o"},
    )
    assert metric_value == result["total_spend_cents"]
    assert result["soft_alert_triggered"] is False


def test_record_tokens_p95_under_threshold() -> None:
    manager = BudgetManager()
    manager.register_budget("tenant", "project", soft_limit_cents=10_000, hard_limit_cents=20_000)

    manager.record_tokens("tenant", "project", provider="openai:gpt-3.5", tokens=1)

    durations: list[float] = []
    for _ in range(120):
        start = time.perf_counter()
        manager.record_tokens("tenant", "project", provider="openai:gpt-3.5", tokens=1)
        durations.append(time.perf_counter() - start)

    durations.sort()
    index = max(0, int(len(durations) * 0.95) - 1)
    p95 = durations[index]
    assert p95 < 0.005
