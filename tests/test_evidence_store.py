import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from service.evidence import store


@pytest.fixture(autouse=True)
def temp_store(tmp_path, monkeypatch):
    base = tmp_path / "evidence"
    monkeypatch.setattr(store, "BASE_DIR", base)
    monkeypatch.setattr(store, "INDEX_PATH", base / "index.jsonl")
    monkeypatch.setattr(store, "PACKS_DIR", base / "packs")
    store.INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    store.INDEX_PATH.touch()
    yield


def test_put_pack_writes_files_and_catalog(monkeypatch):
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utcnow", lambda: now)
    entry = store.put_pack({"foo": "bar"}, ["line1", "line2"], {"m": 1}, tags=["tag1"])
    pack_dir = store.PACKS_DIR / now.strftime("%Y%m%d") / entry["id"]
    assert (pack_dir / "manifest.json").exists()
    assert (pack_dir / "simulation.jsonl").exists()
    assert (pack_dir / "metrics.json").exists()
    assert (pack_dir / "evidence.zip").exists()
    lines = store.INDEX_PATH.read_text().strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["id"] == entry["id"]


def test_list_packs_filter_by_date_and_tag(monkeypatch):
    t1 = datetime(2024, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2024, 1, 2, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utcnow", lambda: t1)
    e1 = store.put_pack({"a": 1}, [], {}, tags=["a"])
    monkeypatch.setattr(store, "_utcnow", lambda: t2)
    e2 = store.put_pack({"b": 1}, [], {}, tags=["b"])
    res_tag = store.list_packs(tag="a")
    assert [r["id"] for r in res_tag] == [e1["id"]]
    start_iso = t2.isoformat().replace("+00:00", "Z")
    res_start = store.list_packs(start=start_iso)
    assert [r["id"] for r in res_start] == [e2["id"]]


def test_get_pack_verifies_sha_and_size(monkeypatch):
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utcnow", lambda: now)
    entry = store.put_pack({"x": 1}, ["l"], {"y": 2})
    got = store.get_pack(entry["id"])
    assert got["manifest"]["x"] == 1
    zip_path = Path(got["paths"]["zip"])
    zip_path.write_bytes(b"tamper")
    with pytest.raises(ValueError):
        store.get_pack(entry["id"])


def test_route_explain_shape(monkeypatch):
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utcnow", lambda: now)
    entry = store.put_pack({"x": 1}, [], {}, tags=["t"])
    explain = store.to_route_explain(entry)
    assert explain == {
        "evidence_id": entry["id"],
        "sha256": entry["sha256_zip"],
        "size_zip": entry["size_zip"],
        "tags": ["t"],
    }


def test_no_pii_or_secrets_in_catalog_or_files(monkeypatch):
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(store, "_utcnow", lambda: now)
    manifest = {"pii_raw": "secret", "ok": {"inner_token": "s", "keep": 1}}
    metrics = {"val": 1, "api_secret": "x", "nested": {"child_token": "y"}}
    entry = store.put_pack(manifest, [], metrics)
    pack_dir = store.PACKS_DIR / now.strftime("%Y%m%d") / entry["id"]
    manifest_data = json.loads((pack_dir / "manifest.json").read_text())
    metrics_data = json.loads((pack_dir / "metrics.json").read_text())
    assert "pii_raw" not in manifest_data
    assert "inner_token" not in manifest_data["ok"]
    assert "api_secret" not in metrics_data
    assert "child_token" not in metrics_data["nested"]
    line = store.INDEX_PATH.read_text().strip()
    assert "pii_raw" not in line and "api_secret" not in line


def test_list_packs_p95_under_500ms_with_1k_items():
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    lines = []
    for i in range(1000):
        ts = (now + timedelta(seconds=i)).isoformat().replace("+00:00", "Z")
        entry = {
            "id": f"id{i}",
            "ts": ts,
            "tags": [],
            "sha256_zip": "0" * 64,
            "size_zip": 1,
            "paths": {"zip": "dummy"},
        }
        lines.append(json.dumps(entry, separators=(",", ":")))
    store.INDEX_PATH.write_text("\n".join(lines) + "\n")
    start = time.perf_counter()
    res = store.list_packs(limit=100)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 500
    assert len(res) == 100
    assert res[0]["id"] == "id999"
