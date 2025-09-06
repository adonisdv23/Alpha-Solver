import os, json
from pathlib import Path
from alpha.core import runner


def test_snapshot_shortlist(tmp_path, monkeypatch):
    monkeypatch.setenv('ALPHA_ARTIFACTS_DIR', str(tmp_path))
    monkeypatch.setenv('ALPHA_SNAPSHOT_TOPK', '2')
    shortlist = [
        {'id': 'tool.a', 'score': 0.9, 'prior': 0.1},
        {'id': 'tool.b', 'score': 0.8, 'prior': 0.2},
        {'id': 'tool.c', 'score': 0.7, 'prior': 0.0},
    ]
    path = runner.snapshot_shortlist('US', 'abc123', shortlist)
    p = Path(path)
    assert p.is_file()
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['region'] == 'US' and data['query_hash'] == 'abc123'
    ids = [it['tool_id'] for it in data['items']]
    assert ids == ['tool.a', 'tool.b']
    assert data['items'][0]['rank'] == 1
