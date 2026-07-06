"""Tests for the local-only operator run capture harness."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from alpha.eval import operator_run_capture as orc

FIXTURES = Path(__file__).parent / "fixtures" / "operator_run_capture"
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "operator_run_capture.py"


def _case_packet() -> dict:
    return json.loads((FIXTURES / "case_packet.json").read_text(encoding="utf-8"))


def _filled_capture() -> dict:
    return json.loads((FIXTURES / "filled_capture.json").read_text(encoding="utf-8"))


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(SCRIPT.parents[1]),
    )


class TestCasePacketValidation:
    def test_fixture_packet_is_valid(self):
        assert orc.validate_case_packet(_case_packet()) == []

    def test_missing_packet_id(self):
        packet = _case_packet()
        del packet["packet_id"]
        errors = orc.validate_case_packet(packet)
        assert any("missing required keys" in error for error in errors)

    def test_duplicate_task_ids_rejected(self):
        packet = _case_packet()
        packet["cases"][1]["task_id"] = packet["cases"][0]["task_id"]
        errors = orc.validate_case_packet(packet)
        assert any("duplicate task_id" in error for error in errors)

    def test_unknown_keys_rejected(self):
        packet = _case_packet()
        packet["score"] = 5
        packet["cases"][0]["winner"] = "alpha"
        errors = orc.validate_case_packet(packet)
        assert any("unknown keys" in error and "score" in error for error in errors)
        assert any("unknown keys" in error and "winner" in error for error in errors)

    def test_empty_cases_rejected(self):
        packet = _case_packet()
        packet["cases"] = []
        errors = orc.validate_case_packet(packet)
        assert any("non-empty list" in error for error in errors)


class TestScaffold:
    def test_scaffold_preserves_task_ids_and_prompts(self):
        packet = _case_packet()
        capture = orc.scaffold_capture(packet)
        assert capture["schema_version"] == orc.CAPTURE_SCHEMA_VERSION
        assert capture["packet_id"] == packet["packet_id"]
        assert capture["capture_mode"] == orc.CAPTURE_MODE
        assert [case["task_id"] for case in capture["cases"]] == [
            case["task_id"] for case in packet["cases"]
        ]
        for entry in capture["cases"]:
            assert entry["baseline_output"] == ""
            assert entry["routed_output"] == ""
            assert entry["route_metadata"] == {}
            assert entry["validation_status"] == "pending"

    def test_scaffold_rejects_invalid_packet(self):
        with pytest.raises(ValueError, match="invalid case packet"):
            orc.scaffold_capture({"cases": []})


class TestCaptureValidation:
    def test_filled_fixture_is_export_ready(self):
        assert orc.validate_capture(_filled_capture(), for_export=True) == []

    def test_scaffold_is_valid_but_not_export_ready(self):
        capture = orc.scaffold_capture(_case_packet())
        assert orc.validate_capture(capture) == []
        errors = orc.validate_capture(capture, for_export=True)
        assert any("still pending" in error for error in errors)

    def test_captured_case_requires_outputs_and_metadata(self):
        capture = _filled_capture()
        capture["cases"][0]["baseline_output"] = "   "
        capture["cases"][0]["route_metadata"] = {}
        errors = orc.validate_capture(capture)
        assert any("non-empty baseline_output" in error for error in errors)
        assert any("route_metadata as a non-empty object" in error for error in errors)

    def test_excluded_case_requires_reason(self):
        capture = _filled_capture()
        del capture["cases"][2]["exclusion_reason"]
        errors = orc.validate_capture(capture)
        assert any("non-empty exclusion_reason" in error for error in errors)

    def test_export_requires_at_least_one_captured_case(self):
        capture = _filled_capture()
        for case in capture["cases"]:
            case["validation_status"] = "excluded"
            case["exclusion_reason"] = "all excluded for the test"
        errors = orc.validate_capture(capture, for_export=True)
        assert any("at least one case" in error for error in errors)

    def test_unknown_case_keys_rejected(self):
        capture = _filled_capture()
        capture["cases"][0]["blind_label"] = "A"
        errors = orc.validate_capture(capture)
        assert any(
            "unknown keys" in error and "blind_label" in error for error in errors
        )

    def test_schema_level_unknown_boundary_keys_rejected(self):
        capture = _filled_capture()
        capture["rank"] = 1
        capture["cases"][0]["source_map"] = {"A": "baseline"}
        errors = orc.validate_capture(capture)
        assert any("unknown keys" in error and "rank" in error for error in errors)
        assert any(
            "unknown keys" in error and "source_map" in error for error in errors
        )

    def test_route_metadata_remains_schema_light_for_route_facts(self):
        capture = _filled_capture()
        capture["cases"][0]["route_metadata"] = {
            "selected_route": "portable",
            "fallbacks_observed": [],
            "operator_note": "route facts recorded during manual capture",
        }
        assert orc.validate_capture(capture, for_export=True) == []
        packet = orc.build_evidence_packet(capture)
        exported_metadata = packet["cases"][0]["route_metadata"]
        assert exported_metadata["selected_route"] == "portable"
        assert exported_metadata["fallbacks_observed"] == []

    def test_wrong_schema_version_rejected(self):
        capture = _filled_capture()
        capture["schema_version"] = "operator_run_capture/v0"
        errors = orc.validate_capture(capture)
        assert any("schema_version" in error for error in errors)


class TestEvidencePacket:
    def test_packet_structure_and_counts(self):
        packet = orc.build_evidence_packet(_filled_capture())
        assert packet["schema_version"] == orc.PACKET_SCHEMA_VERSION
        assert packet["lane_id"] == orc.LANE_ID
        assert packet["packet_id"] == "ORC-FIXTURE-001"
        assert packet["counts"] == {"captured": 2, "excluded": 1, "total": 3}
        assert packet["harness_boundaries"] == orc.HARNESS_BOUNDARIES
        assert all(value is False for value in packet["harness_boundaries"].values())

    def test_cases_sorted_by_task_id(self):
        capture = _filled_capture()
        capture["cases"].reverse()
        packet = orc.build_evidence_packet(capture)
        task_ids = [case["task_id"] for case in packet["cases"]]
        assert task_ids == sorted(task_ids)

    def test_export_bytes_are_deterministic(self):
        first = orc.render_json_bytes(orc.build_evidence_packet(_filled_capture()))
        shuffled = _filled_capture()
        shuffled["cases"].reverse()
        second = orc.render_json_bytes(orc.build_evidence_packet(shuffled))
        assert first == second
        assert first.endswith(b"\n")

    def test_digest_verifies_and_detects_tampering(self):
        packet = orc.build_evidence_packet(_filled_capture())
        assert orc.verify_packet_digest(packet)
        tampered = copy.deepcopy(packet)
        tampered["cases"][0]["routed_output"] = "edited after export"
        assert not orc.verify_packet_digest(tampered)

    def test_build_rejects_incomplete_capture(self):
        with pytest.raises(ValueError, match="invalid capture"):
            orc.build_evidence_packet(orc.scaffold_capture(_case_packet()))


class TestCli:
    def test_init_validate_export_roundtrip(self, tmp_path: Path):
        capture_path = tmp_path / "capture.json"
        packet_path = tmp_path / "packet.json"

        result = _run_cli(
            "init",
            "--case-packet",
            str(FIXTURES / "case_packet.json"),
            "--out",
            str(capture_path),
        )
        assert result.returncode == 0, result.stderr
        assert "OK scaffolded capture" in result.stdout

        result = _run_cli("validate", "--capture", str(capture_path))
        assert result.returncode == 0, result.stderr

        result = _run_cli("validate", "--capture", str(capture_path), "--for-export")
        assert result.returncode == 1
        assert "still pending" in result.stdout

        filled_path = tmp_path / "filled.json"
        filled_path.write_text(
            json.dumps(_filled_capture()), encoding="utf-8"
        )
        result = _run_cli(
            "export", "--capture", str(filled_path), "--out", str(packet_path)
        )
        assert result.returncode == 0, result.stderr
        assert "content_digest: sha256:" in result.stdout

        exported = json.loads(packet_path.read_text(encoding="utf-8"))
        assert orc.verify_packet_digest(exported)

    def test_export_refuses_overwrite_without_force(self, tmp_path: Path):
        filled_path = tmp_path / "filled.json"
        filled_path.write_text(json.dumps(_filled_capture()), encoding="utf-8")
        packet_path = tmp_path / "packet.json"
        packet_path.write_text("existing", encoding="utf-8")
        result = _run_cli(
            "export", "--capture", str(filled_path), "--out", str(packet_path)
        )
        assert result.returncode == 2
        assert "refusing to overwrite" in result.stderr
        assert packet_path.read_text(encoding="utf-8") == "existing"

    def test_missing_input_file_is_usage_error(self, tmp_path: Path):
        result = _run_cli("validate", "--capture", str(tmp_path / "missing.json"))
        assert result.returncode == 2
        assert "not found" in result.stderr
