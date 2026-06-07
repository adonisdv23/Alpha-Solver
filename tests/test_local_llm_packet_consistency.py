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


def test_current_repo_local_llm_packets_pass_packet_consistency_check():
    packet_dirs = iter_packet_dirs()

    assert packet_dirs, "expected local LLM solver orchestration packet dirs"
    assert check_packet_consistency(packet_dirs) == []


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
