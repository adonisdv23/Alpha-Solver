import json
from scripts import telemetry_leaderboard as tl


def test_aggregator_markdown(tmp_path):
    src = tmp_path / "telemetry.jsonl"
    rows = [
        {"type": "run_header", "run_id": "r1"},
        {"solver": "a", "status": "success"},
        {"solver": "b", "status": "success"},
        {"solver": "b", "status": "fail"},
        {"solver": "a", "status": True},
    ]
    src.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    counts = tl.collect([str(src)])
    md = tl.render_markdown(counts, topk=5)
    assert "Telemetry Leaderboard" in md
    assert "Global Top Tools" in md
    assert "| a | 2 |" in md
    assert "| b | 1 |" in md
