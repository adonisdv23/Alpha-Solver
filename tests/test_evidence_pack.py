import json
import os
import zipfile

from service.budget.simulator import load_cost_models, simulate
from service.evidence.collector import pack


def _run_sim():
    models = load_cost_models()
    items = [
        {"id": "1", "prompt_tokens": 100, "completion_tokens": 50, "latency_ms": 100.0},
        {"id": "2", "prompt_tokens": 200, "completion_tokens": 100, "latency_ms": 200.0},
    ]
    return simulate(items, models, provider="openai", model="gpt-4o-mini")


def test_pack_writes_manifest_metrics_and_jsonl(tmp_path):
    sim = _run_sim()
    out = pack(sim, meta={"id": "run1"}, out_dir=str(tmp_path))
    evidence_dir = tmp_path / "evidence"
    assert (evidence_dir / "manifest.json").exists()
    assert (evidence_dir / "metrics.json").exists()
    assert (evidence_dir / "simulation.jsonl").exists()
    assert os.path.exists(out)


def test_manifest_has_hashes_and_counts(tmp_path):
    sim = _run_sim()
    pack(sim, meta={"id": "run1"}, out_dir=str(tmp_path))
    evidence_dir = tmp_path / "evidence"
    manifest = json.loads((evidence_dir / "manifest.json").read_text())
    sim_hash = (evidence_dir / "simulation.jsonl").read_bytes()
    metrics_hash = (evidence_dir / "metrics.json").read_bytes()
    import hashlib

    def sha(data):
        h = hashlib.sha256(); h.update(data); return h.hexdigest()

    assert manifest["counts"]["items"] == 2
    assert manifest["counts"]["tokens"] == 450
    assert manifest["sha256"]["simulation.jsonl"] == sha(sim_hash)
    assert manifest["sha256"]["metrics.json"] == sha(metrics_hash)


def test_jsonl_lines_are_sorted_and_sanitized(tmp_path):
    sim = _run_sim()
    for item in sim["items"]:
        item["user_pii"] = "secret"
        item["pii_raw"] = "secret"
    pack(sim, meta={"id": "run1"}, out_dir=str(tmp_path))
    lines = (tmp_path / "evidence" / "simulation.jsonl").read_text().strip().splitlines()
    ids = [json.loads(line)["id"] for line in lines]
    assert ids == sorted(ids)
    for line in lines:
        data = json.loads(line)
        assert all("pii" not in key for key in data.keys())


def test_zip_contains_expected_files(tmp_path):
    sim = _run_sim()
    zip_path = pack(sim, meta={"id": "run1"}, out_dir=str(tmp_path))
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
    assert {"manifest.json", "metrics.json", "simulation.jsonl"} <= names
