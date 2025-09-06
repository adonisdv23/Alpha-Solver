import os, json
from datetime import datetime, timedelta, timezone
from alpha.core import freshness


def test_parse_and_factor_and_blend(tmp_path):
    p = tmp_path / "priors.json"
    data = {"tool.x":"2025-08-15","tool.y":"2024-08-15T00:00:00Z","bad":"not-a-date"}
    p.write_text(json.dumps(data), encoding="utf-8")
    mp = freshness.load_dated_priors(str(p))
    assert "tool.x" in mp and "tool.y" in mp and "bad" not in mp

    now = datetime(2025, 9, 6, tzinfo=timezone.utc)
    fx_recent = freshness.recency_factor(now - timedelta(days=10), now=now, half_life_days=90)
    fx_old = freshness.recency_factor(now - timedelta(days=365), now=now, half_life_days=90)
    assert 0.0 <= fx_old < fx_recent <= 1.0

    b = freshness.blend(0.6, fx_recent, 0.2)
    assert 0.6 <= b <= 1.0
