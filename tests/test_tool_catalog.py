import json

import pytest

from alpha.tool_catalog import DEFAULT_CATALOG_PATH, DEFAULT_EVIDENCE_BOUNDARY, ToolCatalog, ToolCatalogEntry


def test_tool_catalog_loads_metadata_only_defaults():
    catalog = ToolCatalog.load()

    assert catalog.version == "2026-06-17.tool-catalog-routing-registry-001"
    assert catalog.evidence_boundary == DEFAULT_EVIDENCE_BOUNDARY
    assert catalog.by_tool_id("python_computation") is not None
    assert catalog.by_tool_id("web_current_research") is not None
    assert catalog.by_tool_id("browser_computer_use").enabled_by_default is False
    assert all(tool.execution_authorized is False for tool in catalog.tools)


def test_tool_catalog_entries_have_required_schema_fields():
    entry = ToolCatalog.load().by_tool_id("github_code")

    data = entry.as_dict()
    for field in (
        "tool_id",
        "display_name",
        "task_families",
        "best_for",
        "not_for",
        "requires_network",
        "requires_credentials",
        "privacy_risk",
        "untrusted_input_risk",
        "execution_authorized",
        "enabled_by_default",
        "routing_weight",
        "confidence_effect",
        "evidence_boundary",
        "operator_notes",
    ):
        assert field in data


def test_tool_catalog_rejects_execution_authorized_entry():
    raw = ToolCatalog.load().by_tool_id("python_computation").as_dict()
    raw["execution_authorized"] = True

    with pytest.raises(ValueError, match="must not authorize execution"):
        ToolCatalogEntry.from_mapping(raw)


def test_tool_catalog_rejects_non_metadata_boundary(tmp_path):
    data = json.loads(DEFAULT_CATALOG_PATH.read_text(encoding="utf-8"))
    data["evidence_boundary"] = "can_execute_tools"
    path = tmp_path / "tool_catalog.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="metadata-only"):
        ToolCatalog.load(path)


def test_tool_catalog_rejects_duplicate_ids(tmp_path):
    catalog = ToolCatalog.load()
    data = {
        "version": "test",
        "evidence_boundary": DEFAULT_EVIDENCE_BOUNDARY,
        "tools": [catalog.tools[0].as_dict(), catalog.tools[0].as_dict()],
    }
    path = tmp_path / "tool_catalog.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate tool_id"):
        ToolCatalog.load(path)
