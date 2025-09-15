import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.metrics.aggregator import get_metrics_text


def test_metrics_contains_base_series():
    text = get_metrics_text()
    assert "gate_decisions_total" in text
    assert "replay_pass_total" in text
    assert "budget_spend_cents" in text
    assert "adapter_latency_ms" in text


def test_metrics_extra_counter():
    text = get_metrics_text(extra={"throttles": 2})
    assert "throttles_total" in text
    # Increment again and check value
    text = get_metrics_text(extra={"throttles": 1})
    line = [l for l in text.splitlines() if l.startswith("throttles_total")][0]
    value = float(line.split(" ")[1])
    assert value >= 3
