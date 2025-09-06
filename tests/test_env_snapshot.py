import json
from pathlib import Path

from scripts import env_snapshot


def test_env_snapshot(tmp_path, monkeypatch):
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(tmp_path))
    path = env_snapshot.main()
    p = Path(path)
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ["python", "platform", "paths", "env", "runtime_modules", "file_hashes"]:
        assert key in data
