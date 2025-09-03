import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from alpha.core import loader

REQUIRED_FILES = [
    "sections.yaml",
    "questions.json",
    "risks.json",
    "templates.playbooks.yaml",
    "policy.routes.yaml",
    "tools.json",
    "secrets_vault.json",
    "budget_controls.yaml",
    "audit_trail.json",
    "sla_contracts.yaml",
    "circuit_breakers.json",
    "data_classification.yaml",
    "clusters.yaml",
    "regions.yaml",
]

COUNT_FUNCS = {
    "sections.yaml": lambda d: len(d.get("sections", [])),
    "questions.json": lambda d: sum(len(v) for v in d.get("questions", {}).values()),
    "risks.json": lambda d: len(d.get("risks", [])),
    "templates.playbooks.yaml": lambda d: len(d.get("playbooks", {})),
    "policy.routes.yaml": lambda d: len(d.get("vendors", {})),
    "tools.json": lambda d: len(d.get("tools", [])),
    "secrets_vault.json": lambda d: len(d.get("secrets", [])),
    "budget_controls.yaml": lambda d: 1 if d else 0,
    "audit_trail.json": lambda d: len(d.get("events", [])),
    "sla_contracts.yaml": lambda d: len(d.get("contracts", [])),
    "circuit_breakers.json": lambda d: len(d.get("rules", [])),
    "data_classification.yaml": lambda d: len(d.get("rules", [])),
    "clusters.yaml": lambda d: len(d.get("clusters", [])),
    "regions.yaml": lambda d: len(d.get("regions", [])),
}


def main(base_path: str = "registries"):
    base = Path(base_path)
    loader.load_all(base_path)
    counts = {}
    for fname in REQUIRED_FILES:
        fpath = base / fname
        assert fpath.exists(), f"missing registry file: {fname}"
        data = loader.load_file(fpath)
        func = COUNT_FUNCS.get(fname, lambda d: len(d) if hasattr(d, '__len__') else 0)
        counts[fname] = func(data)
    metrics = {"ok": True, "registries": counts}
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
