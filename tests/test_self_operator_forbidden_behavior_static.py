"""Static proof that forbidden fixtures are scanned as text, not executed."""
from __future__ import annotations

from tests.helpers.self_operator_static_scan import FIXTURE_ROOT, scan_path


def test_fixture_files_are_inert_text_or_json_only() -> None:
    suffixes = {path.name: path.suffixes for path in FIXTURE_ROOT.iterdir() if path.is_file()}
    assert suffixes
    assert all(suffixes[name] in ([".py", ".txt"], [".json"]) for name in suffixes)


def test_scanner_does_not_execute_fixture_code() -> None:
    text_fixture = FIXTURE_ROOT / "forbidden_external_api.py.txt"
    before = text_fixture.read_text(encoding="utf-8")
    findings = scan_path(text_fixture)
    after = text_fixture.read_text(encoding="utf-8")
    assert findings
    assert before == after
    assert not (FIXTURE_ROOT / "EXECUTED_STATIC_FIXTURE_SENTINEL").exists()
