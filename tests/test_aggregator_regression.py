import json
from scripts import telemetry_leaderboard as tl


def test_aggregator_markdown(tmp_path):
    src = tmp_path / "telemetry.jsonl"
    rows = [
        {"event": "run_summary", "run_id": "r1", "task": "a", "final_confidence": 0.9, "final_route": "tot"},
        {"event": "run_summary", "run_id": "r2", "task": "b", "final_confidence": 0.8, "final_route": "cot"},
    ]
    src.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    summaries = tl.collect([str(src)])
    md = tl.render_markdown(summaries, topk=5)
    assert "| r1 | a | 0.900 | tot |" in md
