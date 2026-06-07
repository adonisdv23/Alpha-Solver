"""Tests for the local LLM solver orchestration packet-consistency checker.

The checker is a static docs guard only. These tests do not run local inference,
Ollama, hosted providers, benchmarks, dashboard routes, or /v1/solve.
"""
from pathlib import Path

from scripts.check_local_llm_packet_consistency import (
    CONTROLLED_USAGE_ACCEPTED,
    LEVEL_3_ACCEPTED,
    NO_FURTHER_LEVEL_3,
    OPERATOR_GUIDE_SELECTED_NEXT_LANE,
    check_expected_decisions,
    check_operator_guide,
    check_packet_consistency,
    check_packet_dir,
    iter_packet_dirs,
)


def _write_packet(
    root: Path,
    packet_dir: Path,
    *,
    selected_name: str = "selected-next-lane.md",
    selected_text: str = "`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-NEXT-LANE-001`\n",
    blocker_fallback: bool = True,
    boundary_name: str = "evidence-boundary.md",
) -> None:
    target = root / packet_dir
    target.mkdir(parents=True)
    (target / "README.md").write_text(
        "# Fixture Packet\n\n## Lane\n\n`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-FIXTURE-001`\n",
        encoding="utf-8",
    )
    (target / selected_name).write_text(selected_text, encoding="utf-8")
    if blocker_fallback:
        (target / "blocker-fallback-lane.md").write_text(
            "`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-FIXTURE-FIX-001`\n",
            encoding="utf-8",
        )
    if boundary_name:
        (target / boundary_name).write_text("# Evidence boundary\n", encoding="utf-8")


def _write_expected_decision_context(root: Path) -> None:
    packet_markers = {
        Path(
            "docs/evals/runs/"
            "20260607-local-llm-controlled-usage-operator-run-001/"
            "import-final-decision"
        ): CONTROLLED_USAGE_ACCEPTED,
        Path(
            "docs/evals/runs/"
            "20260607-local-llm-controlled-usage-operator-run-001/closeout"
        ): CONTROLLED_USAGE_ACCEPTED,
        Path(
            "docs/evals/runs/"
            "20260607-local-llm-solver-orchestration-level-3-validation-execution-001/"
            "import-final-decision"
        ): LEVEL_3_ACCEPTED,
        Path(
            "docs/evals/runs/"
            "20260607-local-llm-solver-orchestration-level-3-validation-execution-001/"
            "closeout"
        ): f"{LEVEL_3_ACCEPTED}\n{NO_FURTHER_LEVEL_3}",
    }
    for packet_dir, marker_text in packet_markers.items():
        target = root / packet_dir
        target.mkdir(parents=True)
        (target / "accepted-result.md").write_text(marker_text, encoding="utf-8")

    index_dir = root / "docs/evals/runs/local-llm-solver-orchestration-index"
    index_dir.mkdir(parents=True)
    (index_dir / "decision-ledger.md").write_text(
        f"{CONTROLLED_USAGE_ACCEPTED}\n{LEVEL_3_ACCEPTED}\n{NO_FURTHER_LEVEL_3}\n",
        encoding="utf-8",
    )
    (index_dir / "lane-map.md").write_text(f"{NO_FURTHER_LEVEL_3}\n", encoding="utf-8")


def test_current_repo_local_llm_packets_pass_packet_consistency_check():
    packet_dirs = iter_packet_dirs()

    assert packet_dirs, "expected local LLM solver orchestration packet dirs"
    assert check_packet_consistency(packet_dirs) == []


def test_default_discovery_includes_release_readiness_ladder_packet():
    packet_dirs = iter_packet_dirs()

    assert (
        Path("docs/evals/runs/alpha-solver-post-level-3-release-readiness-ladder")
        in packet_dirs
    )


def test_default_discovery_includes_future_post_level_3_level_4_packet(tmp_path):
    packet_dir = Path(
        "docs/evals/runs/"
        "alpha-solver-post-level-3-level-4-pre-product-surface-requirements"
    )
    _write_packet(
        tmp_path,
        packet_dir,
        selected_text=(
            "`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-4-"
            "PRE-PRODUCT-SURFACE-REQUIREMENTS-NEXT-001`\n"
        ),
    )

    assert iter_packet_dirs(tmp_path) == [packet_dir]


def test_default_discovery_excludes_post_level_3_source_artifact_payloads(tmp_path):
    packet_dir = Path("docs/evals/runs/alpha-solver-post-level-3-fixture")
    nested_source_artifact_dir = packet_dir / "source-artifact"
    named_source_artifact_dir = Path(
        "docs/evals/runs/alpha-solver-post-level-3-source-artifact-fixture"
    )
    suffix_source_artifact_dir = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-4-source-artifact"
    )
    _write_packet(tmp_path, packet_dir)
    _write_packet(tmp_path, nested_source_artifact_dir)
    _write_packet(tmp_path, named_source_artifact_dir)
    _write_packet(tmp_path, suffix_source_artifact_dir)

    packet_dirs = iter_packet_dirs(tmp_path)

    assert packet_dir in packet_dirs
    assert nested_source_artifact_dir not in packet_dirs
    assert named_source_artifact_dir not in packet_dirs
    assert suffix_source_artifact_dir not in packet_dirs
    assert not any(
        part == "source-artifact" or part.endswith("-source-artifact")
        for path in packet_dirs
        for part in path.parts
    )


def test_no_further_lanes_with_selected_implementation_lane_fails(tmp_path):
    packet_dir = Path(
        "docs/evals/runs/"
        "20260607-local-llm-solver-orchestration-level-3-validation-frozen-packet"
    )
    _write_packet(
        tmp_path,
        packet_dir,
        selected_name="selected-next-action.md",
        selected_text=(
            f"`{NO_FURTHER_LEVEL_3}`\n\n"
            "`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-001`\n"
        ),
    )

    findings = check_packet_dir(packet_dir, tmp_path)

    assert any("no-further-lanes" in finding.message for finding in findings)


def test_missing_required_blocker_fallback_fails_when_pattern_requires_one(tmp_path):
    packet_dir = Path("docs/evals/runs/example-local-llm-solver-orchestration-fixture")
    _write_packet(tmp_path, packet_dir, blocker_fallback=False)
    (tmp_path / packet_dir / "README.md").write_text(
        "# Fixture Packet\n\n## Blocker fallback lane\n\nRequired by packet pattern.\n",
        encoding="utf-8",
    )

    findings = check_packet_dir(packet_dir, tmp_path)

    assert any(
        "missing required blocker-fallback-lane.md" == finding.message
        for finding in findings
    )


def test_required_marker_only_in_checks_run_does_not_satisfy_expected_decisions(tmp_path):
    _write_expected_decision_context(tmp_path)
    packet_dir = Path(
        "docs/evals/runs/"
        "20260607-local-llm-solver-orchestration-level-3-validation-execution-001/"
        "closeout"
    )
    (tmp_path / packet_dir / "accepted-result.md").write_text(
        LEVEL_3_ACCEPTED, encoding="utf-8"
    )
    (tmp_path / packet_dir / "checks-run.md").write_text(
        f'`rg "{NO_FURTHER_LEVEL_3}" docs/evals/runs/.../closeout`\n',
        encoding="utf-8",
    )

    findings = check_expected_decisions(tmp_path)

    assert any(
        finding.path == packet_dir
        and f"missing expected decision marker {NO_FURTHER_LEVEL_3}"
        == finding.message
        for finding in findings
    )


def test_required_marker_in_authoritative_status_file_satisfies_expected_decisions(tmp_path):
    _write_expected_decision_context(tmp_path)
    packet_dir = Path(
        "docs/evals/runs/"
        "20260607-local-llm-solver-orchestration-level-3-validation-execution-001/"
        "closeout"
    )
    (tmp_path / packet_dir / "accepted-result.md").write_text(
        LEVEL_3_ACCEPTED, encoding="utf-8"
    )
    (tmp_path / packet_dir / "final-status.md").write_text(
        NO_FURTHER_LEVEL_3, encoding="utf-8"
    )

    assert check_expected_decisions(tmp_path) == []


def test_stale_operator_guide_next_lane_state_fails(tmp_path):
    path = tmp_path / OPERATOR_GUIDE_SELECTED_NEXT_LANE
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Selected Next Lane\n\n"
        f"`{LEVEL_3_ACCEPTED}`\n\n"
        f"`{NO_FURTHER_LEVEL_3}`\n\n"
        "`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-ROADMAP-IMPLEMENTATION-001`\n",
        encoding="utf-8",
    )

    findings = check_operator_guide(tmp_path)

    assert any("selects a future ALPHA lane" in finding.message for finding in findings)


def test_expected_final_decision_markers_are_present_in_current_repo():
    findings = check_packet_consistency(iter_packet_dirs())

    assert findings == []
    packet_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in Path("docs/evals/runs").rglob("*.md")
        if "source-artifact" not in path.parts
    )
    assert CONTROLLED_USAGE_ACCEPTED in packet_text
    assert LEVEL_3_ACCEPTED in packet_text
    assert NO_FURTHER_LEVEL_3 in packet_text
