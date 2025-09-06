import json
import zipfile

from scripts import bundle_artifacts


def test_bundle_artifacts(tmp_path, monkeypatch):
    art = tmp_path / "artifacts"
    sl_dir = art / "shortlists" / "us"
    sl_dir.mkdir(parents=True)
    (sl_dir / "a.json").write_text(json.dumps({"region": "US"}), encoding="utf-8")
    (sl_dir / "b.json").write_text(json.dumps({"region": "US"}), encoding="utf-8")
    (art / "leaderboard.md").write_text("# lb", encoding="utf-8")
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(art))

    bundle_path = bundle_artifacts.bundle_artifacts(art)
    assert bundle_path.exists()
    with zipfile.ZipFile(bundle_path) as zf:
        names = zf.namelist()
        assert "leaderboard.md" in names
        assert "shortlists/us/a.json" in names
