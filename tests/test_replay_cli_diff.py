"""Tests for the observability replay CLI and diff helpers."""

import json
from pathlib import Path
from typing import List

from service.observability import diff as diff_mod
from service.observability import replay_cli


def _write_log(path: Path, events: List[dict]) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        for event in events:
            fp.write(json.dumps(event) + "\n")


def test_replay_cli_prints_events(tmp_path, capsys):
    log_path = tmp_path / "log.jsonl"
    events = [{"name": "a", "route_explain": {"decision": "allow", "confidence": 1.0, "budget_verdict": "ok"}}]
    _write_log(log_path, events)

    replay_cli.main([str(log_path)])
    out = capsys.readouterr().out.strip()
    assert "allow" in out


def test_replay_cli_diff(tmp_path, capsys):
    log_a = tmp_path / "a.jsonl"
    log_b = tmp_path / "b.jsonl"
    events_a = [{"name": "a", "route_explain": {"decision": "allow", "confidence": 1.0, "budget_verdict": "ok"}}]
    events_b = [{"name": "a", "route_explain": {"decision": "deny", "confidence": 0.2, "budget_verdict": "fail"}}]
    _write_log(log_a, events_a)
    _write_log(log_b, events_b)

    replay_cli.main([str(log_a), "--diff", str(log_b)])
    out = capsys.readouterr().out
    assert "-" in out and "+" in out

    diff_text = diff_mod.diff_logs(str(log_a), str(log_b))
    assert "deny" in diff_text
