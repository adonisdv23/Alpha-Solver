import hashlib
import json
import zipfile
from pathlib import Path

from scripts import bundle_artifacts


def test_bundle_v2(tmp_path, monkeypatch):
    art = tmp_path / "artifacts"
    sl_dir = art / "shortlists" / "us"
    env_dir = art / "env"
    run_dir = art / "run"
    sl_dir.mkdir(parents=True)
    env_dir.mkdir(parents=True)
    run_dir.mkdir(parents=True)
    (sl_dir / "a.json").write_text(json.dumps({"tool_id": "a"}), encoding="utf-8")
    (env_dir / "env.json").write_text(json.dumps({}), encoding="utf-8")
    (run_dir / "run.json").write_text(json.dumps({}), encoding="utf-8")
    (art / "leaderboard.md").write_text("lb", encoding="utf-8")
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    (schemas / "foo.schema.json").write_text("{}", encoding="utf-8")
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(art))
    monkeypatch.chdir(tmp_path)
    bundle_path, sha_path = bundle_artifacts.bundle_artifacts(art)
    assert bundle_path.exists() and sha_path.exists()
    with zipfile.ZipFile(bundle_path) as zf:
        names = zf.namelist()
        assert "leaderboard.md" in names
        assert "shortlists/us/a.json" in names
        assert "env/env.json" in names
        assert "run/run.json" in names
        assert "schemas/foo.schema.json" in names
    checksum = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
    assert sha_path.read_text(encoding="utf-8").strip() == checksum
