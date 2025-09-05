import json
from scripts import validate_registry


def test_validate_registry_valid(tmp_path):
    reg = tmp_path / "regs"
    reg.mkdir()
    (reg / "good.json").write_text(json.dumps([{"id": "a"}]))
    assert validate_registry.validate_all(reg) == 0


def test_validate_registry_invalid(tmp_path):
    reg = tmp_path / "regs"
    reg.mkdir()
    (reg / "bad.json").write_text(json.dumps([{"no": "id"}]))
    assert validate_registry.validate_all(reg) == 1
