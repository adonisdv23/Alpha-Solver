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


# ---------------------------------------------------------------------------
# Substantive Lift preflight
# (OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001)
# ---------------------------------------------------------------------------

ANCHORED_PROMPT = (
    "Decide whether `tests/fixtures/demo_plan.json` gains a rollback step "
    "before the PR #701 review."
)

# Passes the prompt-aware checker: every line names a case object from the
# anchored prompt. Synthetic operator-authored text; not a model output.
ANCHORED_PASS_BLOCK = """Intent: Choose whether the rollback step lands in tests/fixtures/demo_plan.json before the PR #701 review window.
Assumes: The packet in tests/fixtures/demo_plan.json is the only artifact reviewers exercise before PR #701.
Tradeoff: Adding rollback coverage to tests/fixtures/demo_plan.json now versus keeping PR #701 small enough to review in one pass.
Recommendation: Add the rollback step to tests/fixtures/demo_plan.json now and keep PR #701 limited to that packet change.
Fails if: The rollback step needs fields that tests/fixtures/demo_plan.json cannot carry without breaking the packet loader.
Next: Draft the rollback entry in tests/fixtures/demo_plan.json and attach it to the PR #701 description today."""

# Structurally shaped six-move block with no case objects at all: fails the
# prompt-aware checker for an anchored prompt, but is a legitimate pass when
# the prompt itself has no extractable anchors (vacuous anchor checks).
GENERIC_BLOCK = """Intent: Decide the best path forward for the team given the stated goal.
Assumes: The strongest hidden assumption is that the current process is stable.
Tradeoff: Speed of delivery versus completeness of the final outcome.
Recommendation: Proceed with the smaller change under the current constraints.
Fails if: The requirements change materially before the work completes.
Next: Write down the decision and share it with the owning group today."""

ANCHOR_FREE_PROMPT = "Should our weekly status update lead with wins or with risks?"

PROHIBITED_KEY_MARKERS = (
    "score",
    "rank",
    "winner",
    "blind",
    "source_map",
    "identity_map",
)


def _preflight_case(task_id: str, prompt: str, routed_output: str, **overrides) -> dict:
    case = {
        "task_id": task_id,
        "prompt": prompt,
        "baseline_output": "baseline text placeholder",
        "routed_output": routed_output,
        "route_metadata": {"source": "unit-test synthetic case"},
        "validation_status": "captured",
    }
    case.update(overrides)
    return case


def _preflight_capture(cases: list) -> dict:
    return {
        "schema_version": orc.CAPTURE_SCHEMA_VERSION,
        "packet_id": "lift-preflight-tests",
        "capture_mode": orc.CAPTURE_MODE,
        "cases": cases,
    }


def _walk_keys(payload):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key
            yield from _walk_keys(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _walk_keys(item)


class TestLiftPreflight:
    def test_anchored_compliant_routed_output_passes(self):
        capture = _preflight_capture(
            [_preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK)]
        )
        report = orc.lift_preflight_capture(capture)
        finding = report["cases"][0]
        assert finding["state"] == "structural_pass"
        assert finding["anchor_checks_vacuous"] is False
        assert finding["case_anchor_count"] >= 2
        assert finding["structural_flags"] == []
        assert report["summary"]["needs_attention"] == []

    def test_generic_block_fails_for_anchored_prompt(self):
        capture = _preflight_capture(
            [_preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK)]
        )
        report = orc.lift_preflight_capture(capture)
        finding = report["cases"][0]
        assert finding["state"] == "structural_fail"
        assert "unanchored_lift" in finding["structural_flags"]
        assert report["summary"]["needs_attention"] == ["case-b"]

    def test_anchor_free_prompt_is_vacuous_not_a_false_failure(self):
        capture = _preflight_capture(
            [_preflight_case("case-c", ANCHOR_FREE_PROMPT, GENERIC_BLOCK)]
        )
        report = orc.lift_preflight_capture(capture)
        finding = report["cases"][0]
        assert finding["state"] == "structural_pass"
        assert finding["anchor_checks_vacuous"] is True
        assert finding["case_anchor_count"] == 0
        assert report["summary"]["needs_attention"] == []

    def test_excluded_case_is_skipped_not_checked(self):
        capture = _preflight_capture(
            [
                _preflight_case(
                    "case-d",
                    ANCHORED_PROMPT,
                    "",
                    validation_status="excluded",
                    exclusion_reason="operator dropped this task",
                )
            ]
        )
        report = orc.lift_preflight_capture(capture)
        finding = report["cases"][0]
        assert finding["state"] == "excluded_case"
        assert "checker" not in finding
        assert report["summary"]["needs_attention"] == []

    def test_missing_prompt_and_missing_routed_output_states(self):
        capture = _preflight_capture(
            [
                _preflight_case("case-e", "", GENERIC_BLOCK),
                _preflight_case(
                    "case-f", ANCHORED_PROMPT, "", validation_status="pending"
                ),
            ]
        )
        report = orc.lift_preflight_capture(capture)
        states = {f["task_id"]: f["state"] for f in report["cases"]}
        assert states == {
            "case-e": "missing_prompt",
            "case-f": "missing_routed_output",
        }
        assert report["summary"]["needs_attention"] == ["case-e", "case-f"]

    def test_safe_out_routed_output_is_not_applicable(self):
        sys.path.insert(0, str(SCRIPT.parents[1]))
        from alpha_solver_portable import PORTABLE_LOCAL_UNSUPPORTED_SAFEOUT

        capture = _preflight_capture(
            [
                _preflight_case(
                    "case-g", ANCHORED_PROMPT, PORTABLE_LOCAL_UNSUPPORTED_SAFEOUT
                )
            ]
        )
        report = orc.lift_preflight_capture(capture)
        finding = report["cases"][0]
        assert finding["state"] == "safe_out_not_applicable"
        assert "checker" not in finding
        assert report["summary"]["needs_attention"] == []

    def test_preflight_does_not_mutate_capture(self):
        capture = _preflight_capture(
            [
                _preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK),
                _preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK),
            ]
        )
        snapshot = copy.deepcopy(capture)
        orc.lift_preflight_capture(capture)
        assert capture == snapshot

    def test_report_carries_boundary_and_no_prohibited_fields(self):
        capture = _preflight_capture(
            [
                _preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK),
                _preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK),
                _preflight_case("case-c", ANCHOR_FREE_PROMPT, GENERIC_BLOCK),
            ]
        )
        report = orc.lift_preflight_capture(capture)
        assert report["boundary"] == orc.LIFT_PREFLIGHT_BOUNDARY
        assert "not answer quality" in report["boundary"]
        assert report["schema_version"] == orc.LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION
        assert report["schema_version"] != orc.PACKET_SCHEMA_VERSION
        assert report["schema_version"] != orc.CAPTURE_SCHEMA_VERSION
        for key in _walk_keys(report):
            for marker in PROHIBITED_KEY_MARKERS:
                assert marker not in key.lower(), key

    def test_summary_counts_cover_all_states(self):
        capture = _preflight_capture(
            [
                _preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK),
                _preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK),
                _preflight_case(
                    "case-d",
                    ANCHORED_PROMPT,
                    "",
                    validation_status="excluded",
                    exclusion_reason="dropped",
                ),
            ]
        )
        report = orc.lift_preflight_capture(capture)
        counts = report["summary"]["counts"]
        assert set(orc.LIFT_PREFLIGHT_STATES) <= set(counts)
        assert counts["total"] == 3
        assert counts["structural_pass"] == 1
        assert counts["structural_fail"] == 1
        assert counts["excluded_case"] == 1

    def test_invalid_top_level_shapes_are_rejected(self):
        with pytest.raises(ValueError):
            orc.lift_preflight_capture(["not", "a", "dict"])
        with pytest.raises(ValueError):
            orc.lift_preflight_capture({"packet_id": "x", "cases": []})

    def test_non_dict_case_is_flagged_not_crashed(self):
        capture = _preflight_capture(
            [_preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK)]
        )
        capture["cases"].append("not a case object")
        report = orc.lift_preflight_capture(capture)
        assert report["cases"][1]["state"] == "invalid_case"
        assert report["summary"]["needs_attention"] == ["cases[1]"]

    def test_malformed_dict_case_with_compliant_output_is_invalid_case(self):
        case = {
            "prompt": ANCHORED_PROMPT,
            "routed_output": ANCHORED_PASS_BLOCK,
        }
        report = orc.lift_preflight_capture(_preflight_capture([case]))
        finding = report["cases"][0]
        assert finding["state"] == "invalid_case"
        assert "missing required keys" in finding["detail"]
        assert "task_id" in finding["detail"]
        assert "validation_status" in finding["detail"]
        assert "baseline_output" in finding["detail"]
        assert "route_metadata" in finding["detail"]
        assert report["summary"]["needs_attention"] == ["cases[0]"]

    def test_malformed_case_never_returns_structural_pass(self):
        malformed_cases = [
            {"prompt": ANCHORED_PROMPT, "routed_output": ANCHORED_PASS_BLOCK},
            _preflight_case(
                "case-unknown",
                ANCHORED_PROMPT,
                ANCHORED_PASS_BLOCK,
                unexpected="not allowed",
            ),
            _preflight_case(
                "case-status",
                ANCHORED_PROMPT,
                ANCHORED_PASS_BLOCK,
                validation_status="done",
            ),
            _preflight_case(
                "case-metadata",
                ANCHORED_PROMPT,
                ANCHORED_PASS_BLOCK,
                route_metadata=[],
            ),
            _preflight_case(
                "case-excluded",
                ANCHORED_PROMPT,
                "",
                validation_status="excluded",
                exclusion_reason="",
            ),
        ]
        report = orc.lift_preflight_capture(_preflight_capture(malformed_cases))
        assert {finding["state"] for finding in report["cases"]} == {"invalid_case"}
        assert report["summary"]["counts"]["structural_pass"] == 0

    def test_render_text_names_boundary_and_vacuous_anchors(self):
        capture = _preflight_capture(
            [_preflight_case("case-c", ANCHOR_FREE_PROMPT, GENERIC_BLOCK)]
        )
        text = orc.render_lift_preflight_text(orc.lift_preflight_capture(capture))
        assert "Structural wording preflight only" in text
        assert "anchor checks vacuous" in text
        assert "needs attention: none" in text


class TestLiftPreflightCli:
    def _write_capture(self, tmp_path: Path, cases: list) -> Path:
        path = tmp_path / "capture.json"
        path.write_text(json.dumps(_preflight_capture(cases)), encoding="utf-8")
        return path

    def test_passing_capture_exits_zero_with_boundary_language(self, tmp_path: Path):
        capture_path = self._write_capture(
            tmp_path, [_preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK)]
        )
        result = _run_cli("lift-preflight", "--capture", str(capture_path))
        assert result.returncode == 0, result.stderr
        assert "structural_pass" in result.stdout
        assert "Structural wording preflight only" in result.stdout
        assert "not answer quality" in result.stdout

    def test_malformed_compliant_case_exits_one(self, tmp_path: Path):
        capture_path = self._write_capture(
            tmp_path,
            [{"prompt": ANCHORED_PROMPT, "routed_output": ANCHORED_PASS_BLOCK}],
        )
        result = _run_cli("lift-preflight", "--capture", str(capture_path))
        assert result.returncode == 1
        assert "invalid_case" in result.stdout
        assert "structural_pass" not in result.stdout

    def test_structural_fail_exits_one_and_writes_report(self, tmp_path: Path):
        capture_path = self._write_capture(
            tmp_path, [_preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK)]
        )
        report_path = tmp_path / "report.json"
        result = _run_cli(
            "lift-preflight",
            "--capture",
            str(capture_path),
            "--report-out",
            str(report_path),
        )
        assert result.returncode == 1
        assert "structural_fail" in result.stdout
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["cases"][0]["state"] == "structural_fail"
        for key in _walk_keys(report):
            for marker in PROHIBITED_KEY_MARKERS:
                assert marker not in key.lower(), key

    def test_preflight_leaves_capture_bytes_unchanged(self, tmp_path: Path):
        capture_path = self._write_capture(
            tmp_path, [_preflight_case("case-b", ANCHORED_PROMPT, GENERIC_BLOCK)]
        )
        before = capture_path.read_bytes()
        result = _run_cli("lift-preflight", "--capture", str(capture_path))
        assert result.returncode == 1
        assert capture_path.read_bytes() == before

    def test_report_out_refuses_overwrite_without_force(self, tmp_path: Path):
        capture_path = self._write_capture(
            tmp_path, [_preflight_case("case-a", ANCHORED_PROMPT, ANCHORED_PASS_BLOCK)]
        )
        report_path = tmp_path / "report.json"
        report_path.write_text("existing", encoding="utf-8")
        result = _run_cli(
            "lift-preflight",
            "--capture",
            str(capture_path),
            "--report-out",
            str(report_path),
        )
        assert result.returncode == 2
        assert "refusing to overwrite" in result.stderr
        assert report_path.read_text(encoding="utf-8") == "existing"

    def test_existing_init_validate_export_flow_is_untouched(self, tmp_path: Path):
        filled_path = tmp_path / "filled.json"
        filled_path.write_text(json.dumps(_filled_capture()), encoding="utf-8")
        packet_path = tmp_path / "packet.json"
        result = _run_cli(
            "export", "--capture", str(filled_path), "--out", str(packet_path)
        )
        assert result.returncode == 0, result.stderr
        exported = json.loads(packet_path.read_text(encoding="utf-8"))
        assert orc.verify_packet_digest(exported)
        assert "lift_preflight" not in json.dumps(exported)
