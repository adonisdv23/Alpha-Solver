import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PANELS_PATH = REPO_ROOT / "alpha" / "dashboard" / "panels.json"
ALERTS_PATH = REPO_ROOT / "alpha" / "dashboard" / "alerts.json"


@pytest.fixture(scope="module")
def panels_config():
    raw = PANELS_PATH.read_text()
    data = json.loads(raw)
    assert isinstance(data, dict), "panels.json must be a JSON object"
    assert "panels" in data and isinstance(data["panels"], list), "panels.json needs a panels list"
    return data


@pytest.fixture(scope="module")
def alerts_config():
    raw = ALERTS_PATH.read_text()
    data = json.loads(raw)
    assert isinstance(data, dict), "alerts.json must be a JSON object"
    assert "alerts" in data and isinstance(data["alerts"], list), "alerts.json needs an alerts list"
    return data


def validate_promql(expr: str) -> None:
    assert isinstance(expr, str), "PromQL expression must be a string"
    stripped = expr.strip()
    assert stripped, "PromQL expression should not be empty"
    assert stripped == expr, "PromQL expression should not contain leading/trailing whitespace"

    pairs = {")": "(",
        "]": "[",
        "}": "{",
    }
    openers = set(pairs.values())
    stack = []
    for char in expr:
        if char in openers:
            stack.append(char)
        elif char in pairs:
            assert stack, f"Unbalanced bracket near {char}"
            opener = stack.pop()
            assert opener == pairs[char], f"Mismatched {opener} and {char}"
    assert not stack, "PromQL expression has unclosed brackets"

    # Ensure expressions look like PromQL by requiring at least one metric token and a function/operator.
    has_metric = any(part.isidentifier() and part[0].isalpha() for part in stripped.replace("{", " ").replace("}", " ").replace("(", " ").replace(")", " ").split())
    assert has_metric, "PromQL expression should reference at least one metric identifier"
    assert any(op in expr for op in ("sum", "rate", "increase", "quantile", "histogram_quantile", "+", "-", "/", "*")), "PromQL expression missing expected functions"


def test_panels_config_structure(panels_config):
    panels = panels_config["panels"]
    assert len(panels) >= 5, "Expected at least five panels"

    required_metrics = {
        "gate_decisions_total": False,
        "replay_pass_total": False,
        "budget_spend_cents": False,
        "adapter_latency_ms": False,
        "retries_total": False,
        "breaker_open_total": False,
    }

    seen_ids = set()
    for panel in panels:
        assert set(panel.keys()) >= {"id", "title", "type", "datasource", "targets"}
        assert panel["id"], "Panel id must not be empty"
        assert panel["id"] not in seen_ids, "Panel ids should be unique"
        seen_ids.add(panel["id"])

        assert isinstance(panel["targets"], list) and panel["targets"], "Each panel needs at least one target"
        for target in panel["targets"]:
            assert set(target.keys()) >= {"expr", "legend"}
            validate_promql(target["expr"])
            for metric in required_metrics:
                if metric in target["expr"]:
                    required_metrics[metric] = True

    assert all(required_metrics.values()), "Not all required metrics are represented in panels"


def test_alerts_config_structure(alerts_config):
    alerts = alerts_config["alerts"]
    assert alerts, "Expected at least one alert"

    metric_presence = {
        "gate_decisions_total": False,
        "adapter_latency_ms": False,
        "retries_total": False,
        "breaker_open_total": False,
    }

    for alert in alerts:
        assert set(alert.keys()) >= {"name", "expr", "for", "labels", "annotations"}
        assert alert["name"].strip(), "Alert must have a name"
        validate_promql(alert["expr"])
        assert isinstance(alert["labels"], dict), "Alert labels must be a dict"
        assert isinstance(alert["annotations"], dict), "Alert annotations must be a dict"

        for metric in metric_presence:
            if metric in alert["expr"]:
                metric_presence[metric] = True

    for key, present in metric_presence.items():
        assert present, f"Alert coverage missing required metric: {key}"


def test_promql_parses_for_panels_and_alerts(panels_config, alerts_config):
    """Smoke test to ensure every expression is PromQL-ish by checking token balance."""

    panel_exprs = [target["expr"] for panel in panels_config["panels"] for target in panel["targets"]]
    alert_exprs = [alert["expr"] for alert in alerts_config["alerts"]]

    for expr in panel_exprs + alert_exprs:
        validate_promql(expr)
