from pathlib import Path

from alpha.core.loader import load_all, parse_yaml_lite
from alpha.core.policy import PolicyEngine


def test_canonical_registry_classification_policy_loads_and_enforces_expected_tags():
    registries = load_all("registries")
    policy = registries.get("data_classification")

    assert policy["version"] == "0.1.0"
    assert {rule["match"]: rule["action"] for rule in policy["rules"]} == {
        "phi": "mask",
        "pii": "deny",
    }

    engine = PolicyEngine(registries)
    assert engine.classify(["pii"])["allow"] is False
    phi = engine.classify(["phi"])
    assert phi["allow"] is True
    assert phi["masked"] is True


def test_legacy_runtime_config_remains_distinct_from_canonical_registry():
    canonical = load_all("registries")["data_classification"]
    legacy = parse_yaml_lite(Path("config/data_classification.yaml").read_text())

    canonical_actions = {rule["match"]: rule["action"] for rule in canonical["rules"]}
    legacy_actions = {rule["match"]: rule["action"] for rule in legacy["rules"]}

    assert canonical_actions["pii"] == "deny"
    assert legacy_actions["pii|secret|token"] == "instructions_only"


def test_reconciliation_packet_records_precedence_and_enforcement_boundary():
    packet = Path(
        "docs/evals/runs/"
        "alpha-solver-def-002-data-classification-registry-reconciliation-001"
    )
    precedence = (packet / "precedence-map.md").read_text(encoding="utf-8")
    boundary = (packet / "enforcement-boundary.md").read_text(encoding="utf-8")

    assert "registries/data_classification.yaml` is the canonical policy registry" in precedence
    assert "config/data_classification.yaml` is a compatibility runtime input only" in precedence
    assert "No runtime enforcement was changed in this lane" in boundary
