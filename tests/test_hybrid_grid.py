import json
from alpha.core.registry_provider import RegistryProvider


def _write_seed(path):
    rows = [
        {"id": "b", "name": "B", "keywords": ["alpha"], "adoption_prior": 0.5},
        {"id": "a", "name": "A", "keywords": ["alpha"], "adoption_prior": 0.5},
        {"id": "c", "name": "C", "keywords": ["beta"], "adoption_prior": 0.5},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return str(path)


def test_hybrid_grid_deterministic(tmp_path):
    seed = _write_seed(tmp_path / "seed.jsonl")
    rp = RegistryProvider(seed_path=seed)
    r1 = rp.shortlist("alpha", k=3)
    r2 = rp.shortlist("alpha", k=3)
    assert [r["tool_id"] for r in r1] == [r["tool_id"] for r in r2] == ["a", "b", "c"]
    assert r1[0]["tool_id"] == "a"
    assert r1[1]["tool_id"] == "b"
