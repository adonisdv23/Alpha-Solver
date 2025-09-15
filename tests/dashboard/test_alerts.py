import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ALERTS_PATH = REPO_ROOT / "alpha" / "dashboard" / "alerts.json"


@pytest.fixture(scope="module")
def alerts_config():
    raw = ALERTS_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, dict), "alerts.json must be a JSON object"
    assert "alerts" in data and isinstance(data["alerts"], list), "alerts.json requires an alerts list"
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

    tokens = re.split(r"[^A-Za-z0-9_]+", stripped)
    assert any(token and token[0].isalpha() for token in tokens), "PromQL expression should reference at least one metric"
    assert any(operator in expr for operator in ("sum", "rate", "increase", "quantile", "histogram_quantile", "max_over_time", "avg_over_time", "+", "-", "/", "*", ">", "<", ">=", "<=")), "PromQL expression missing expected functions"


def get_alert_by_name(alerts, name):
    for alert in alerts:
        if alert.get("name") == name:
            return alert
    return None


def test_alerts_file_structure(alerts_config):
    assert alerts_config.get("template") == "dashboards_alerts_v1", "alerts.json must declare the dashboards_alerts_v1 template"
    assert alerts_config["alerts"], "alerts.json must contain at least one alert"


def test_alert_entries_have_required_keys(alerts_config):
    for alert in alerts_config["alerts"]:
        assert set(alert.keys()) >= {"name", "expr", "for", "labels", "annotations"}, "Every alert must declare core fields"


def test_alert_names_unique(alerts_config):
    names = [alert["name"] for alert in alerts_config["alerts"]]
    assert len(names) == len(set(names)), "Alert rule names should be unique"


def test_expected_alerts_present(alerts_config):
    alerts = alerts_config["alerts"]
    expected = {
        "Retry Saturation P95 High": "sum(max_over_time(retry_p95{environment=\"prod\"}[10m])) >= 2",
        "Breaker Open Duration P95 High": "sum(max_over_time(breaker_open_p95_ms{environment=\"prod\"}[10m])) >= 100",
        "HTTP 5xx Ratio High": "sum(avg_over_time(http_5xx_ratio{environment=\"prod\"}[5m])) > 0.01",
    }
    for name, expr in expected.items():
        alert = get_alert_by_name(alerts, name)
        assert alert is not None, f"Missing required alert: {name}"
        assert alert["expr"] == expr, f"Unexpected PromQL for {name}"


def test_retry_alert_threshold(alerts_config):
    alert = get_alert_by_name(alerts_config["alerts"], "Retry Saturation P95 High")
    assert alert is not None, "Retry Saturation alert must exist"
    assert ">=" in alert["expr"], "Retry alert must compare against a threshold"
    assert ">= 2" in alert["expr"], "Retry alert threshold must be 2 attempts"
    assert alert["for"] == "15m", "Retry alert must require 15m confirmation window"


def test_breaker_alert_threshold(alerts_config):
    alert = get_alert_by_name(alerts_config["alerts"], "Breaker Open Duration P95 High")
    assert alert is not None, "Breaker alert must exist"
    assert ">= 100" in alert["expr"], "Breaker alert threshold must be 100ms"
    assert alert["for"] == "15m", "Breaker alert must require 15m confirmation window"


def test_http_5xx_alert_threshold(alerts_config):
    alert = get_alert_by_name(alerts_config["alerts"], "HTTP 5xx Ratio High")
    assert alert is not None, "HTTP 5xx alert must exist"
    assert "> 0.01" in alert["expr"], "HTTP 5xx alert threshold must be 1%"
    assert alert["for"] == "10m", "HTTP 5xx alert must require 10m confirmation window"


def test_alert_labels_include_severity(alerts_config):
    for alert in alerts_config["alerts"]:
        labels = alert["labels"]
        assert isinstance(labels, dict) and labels, "Alert labels must be a dict"
        assert "severity" in labels, "Alert labels must include severity"
        assert labels.get("service") == "res_dash", "Alerts must be tagged with the res_dash service"


def test_alert_annotations_have_summary(alerts_config):
    for alert in alerts_config["alerts"]:
        annotations = alert["annotations"]
        assert isinstance(annotations, dict) and annotations, "Alert annotations must be a dict"
        assert "summary" in annotations, "Alert annotations must include a summary"
        assert "runbook" in annotations, "Alert annotations must link to a runbook"


def test_promql_expressions_are_balanced(alerts_config):
    for alert in alerts_config["alerts"]:
        validate_promql(alert["expr"])
