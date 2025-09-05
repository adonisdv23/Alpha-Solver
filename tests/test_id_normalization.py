import json
import pytest
from alpha.core.ids import slugify_tool_id, validate_tool_id
from scripts import preflight


def test_slugify_and_validate():
    slug = slugify_tool_id("Monday.com !")
    assert slug == "monday.com"
    assert validate_tool_id(slug) == slug
    with pytest.raises(ValueError):
        validate_tool_id("Bad ID")


def test_preflight_duplicates(tmp_path, monkeypatch):
    reg_dir = tmp_path / "registries"
    reg_dir.mkdir()
    (reg_dir / "tools.json").write_text(json.dumps([
        {"id": "tool.one"}, {"id": "Tool One"}
    ]), encoding="utf-8")
    art_dir = tmp_path / "artifacts"
    art_dir.mkdir()
    (art_dir / "tools_canon.csv").write_text("id\n", encoding="utf-8")
    monkeypatch.setattr(preflight, "ROOT", tmp_path)
    monkeypatch.setattr(preflight, "REG_DIR", reg_dir)
    monkeypatch.setattr(preflight, "ART_DIR", art_dir)
    assert preflight.main() != 0
