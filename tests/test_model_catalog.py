import copy
import json

import pytest

from alpha.model_catalog import DEFAULT_EVIDENCE_BOUNDARY, ModelCatalog, ModelCatalogEntry


EXPECTED_LOCAL_MODELS = {"qwen2.5:3b", "gemma3:4b", "llama3.2:1b", "llama3.2:latest"}
EXPECTED_OPENAI_MODELS = {"gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini"}
REQUIRED_METADATA_FIELDS = {
    "provider",
    "model_id",
    "display_name",
    "mode",
    "enabled_by_default",
    "routing_roles",
    "task_families",
    "capability_tags",
    "cost_tier",
    "latency_tier",
    "context_tier",
    "privacy_tier",
    "supports_json",
    "supports_tools",
    "supports_vision",
    "smoke_eligible",
    "requires_network",
    "requires_credentials",
    "evidence_boundary",
    "quality_claim",
    "last_reviewed",
    "review_status",
    "operator_notes",
}


def test_catalog_loads_successfully():
    catalog = ModelCatalog.load()

    assert catalog.version
    assert catalog.models
    assert catalog.evidence_boundary == DEFAULT_EVIDENCE_BOUNDARY


def test_catalog_includes_expected_local_models():
    catalog = ModelCatalog.load()

    assert EXPECTED_LOCAL_MODELS <= {model.model_id for model in catalog.by_mode("local", enabled_only=False)}


def test_catalog_includes_expected_openai_models():
    catalog = ModelCatalog.load()

    assert EXPECTED_OPENAI_MODELS <= {model.model_id for model in catalog.by_mode("openai", enabled_only=False)}


def test_each_model_entry_has_required_no_quality_claim_metadata():
    catalog = ModelCatalog.load()

    for model in catalog.models:
        data = model.as_dict()
        assert REQUIRED_METADATA_FIELDS <= set(data)
        assert model.provider
        assert model.mode in {"local", "openai"}
        assert model.model_id
        assert model.routing_roles
        assert model.task_families
        assert model.capability_tags
        assert model.cost_tier in {"low", "medium", "high", "unknown"}
        assert model.latency_tier in {"low", "medium", "high", "unknown"}
        assert model.context_tier in {"low", "medium", "high", "unknown"}
        assert isinstance(model.smoke_eligible, bool)
        assert model.quality_claim is False
        assert model.evidence_boundary == DEFAULT_EVIDENCE_BOUNDARY
        assert model.review_status in {"operator_metadata", "smoke_only"}
        assert "not" in model.operator_notes.lower()


def test_missing_required_metadata_field_is_rejected():
    raw = ModelCatalog.load().models[0].as_dict()
    raw.pop("cost_tier")

    with pytest.raises(ValueError, match="missing required fields"):
        ModelCatalogEntry.from_mapping(raw)


def test_quality_claim_true_is_rejected():
    raw = ModelCatalog.load().models[0].as_dict()
    raw["quality_claim"] = True

    with pytest.raises(ValueError, match="must not carry quality claims"):
        ModelCatalogEntry.from_mapping(raw)


def test_catalog_entries_do_not_imply_validation_evidence():
    catalog = ModelCatalog.load()

    assert all(model.quality_claim is False for model in catalog.models)
    assert all(not any(model.evidence_boundary.values()) for model in catalog.models)
    assert all("validation" not in model.review_status for model in catalog.models)


def test_entry_evidence_boundary_true_is_rejected():
    raw = copy.deepcopy(ModelCatalog.load().models[0].as_dict())
    raw["evidence_boundary"]["quality_evidence"] = True

    with pytest.raises(ValueError, match="must not imply validation evidence"):
        ModelCatalogEntry.from_mapping(raw)


def test_boolean_metadata_string_false_is_rejected():
    raw = ModelCatalog.load().models[0].as_dict()
    raw["quality_claim"] = "false"

    with pytest.raises(ValueError, match="must be boolean"):
        ModelCatalogEntry.from_mapping(raw)


def test_list_metadata_must_be_non_empty_string_list():
    raw = ModelCatalog.load().models[0].as_dict()
    raw["routing_roles"] = "local_preview"

    with pytest.raises(ValueError, match="non-empty string list"):
        ModelCatalogEntry.from_mapping(raw)


def test_duplicate_model_ids_are_rejected(tmp_path):
    catalog = ModelCatalog.load()
    data = {
        "version": "test",
        "evidence_boundary": DEFAULT_EVIDENCE_BOUNDARY,
        "models": [catalog.models[0].as_dict(), catalog.models[0].as_dict()],
    }
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="model_id values must be unique"):
        ModelCatalog.load(path)


def test_catalog_json_uses_required_metadata_names():
    data = json.loads(open("configs/model_catalog.json", encoding="utf-8").read())

    for raw in data["models"]:
        assert REQUIRED_METADATA_FIELDS <= set(raw)
        assert "enabled_default" not in raw
        assert "notes" not in raw
