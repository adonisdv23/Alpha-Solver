from pathlib import Path

from scripts import check_local_llm_doc_paths as checker


def _write(path: Path, text: str = "") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _make_required_tree(root: Path) -> None:
    for rel in checker.REQUIRED_SOURCE_OF_TRUTH_PATHS:
        (root / rel).mkdir(parents=True, exist_ok=True)


def test_existing_valid_local_llm_paths_pass(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    _write(tmp_path / "docs/local_llm_solver_orchestration_operator_guide/README.md")
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/quick-start.md",
        "See `docs/local_llm_solver_orchestration_operator_guide/README.md`.\n"
        "Also see [index](docs/evals/runs/local-llm-solver-orchestration-index/).\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert findings == []


def test_missing_local_llm_packet_path_is_reported(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/quick-start.md",
        "Broken packet: `docs/evals/runs/20260607-local-llm-solver-orchestration-missing-packet/README.md`.\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert len(findings) == 1
    assert "does not exist" in findings[0].message
    assert "missing-packet" in findings[0].reference


def test_non_local_markdown_links_are_ignored_unless_repo_relative(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/examples.md",
        "Ignore [external](https://example.invalid/missing-local-llm-packet).\n"
        "Ignore [anchor](#missing-local-llm-packet).\n"
        "Ignore relative [neighbor](neighbor.md).\n"
        "Ignore non-local repo path `docs/ordinary-missing.md`.\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert findings == []


def test_stale_selected_next_lane_conflict_is_detected(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/selected-next-lane.md",
        "## Selected next action\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-OLD-DOCS-LANE-001\n\n"
        "## Selected next action\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-NEW-DOCS-LANE-001\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert len(findings) == 1
    assert "conflicting selected-next action" in findings[0].message
    assert "NEW-DOCS-LANE" in findings[0].reference


def test_conflicting_current_selected_next_actions_with_fallback_sections_fail(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/selected-next-lane.md",
        "## Selected next action\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-A-001\n\n"
        "## Blocker fallback lane\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-A-FIX-001\n\n"
        "## Selected next action\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-B-001\n\n"
        "## Blocker fallback lane\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-B-FIX-001\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert len(findings) == 1
    assert "CURRENT-B-001" in findings[0].reference
    assert "FIX" not in findings[0].reference


def test_inline_fallback_lane_near_selected_next_does_not_mask_conflict(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/selected-next-lane.md",
        "Selected next action: ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-A-001. "
        "Blocker fallback lane: ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-A-FIX-001.\n"
        "Selected next action: ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-B-001.\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert len(findings) == 1
    assert "CURRENT-B-001" in findings[0].reference
    assert "FIX" not in findings[0].reference


def test_prior_preserved_selected_next_reference_remains_allowed(tmp_path: Path) -> None:
    _make_required_tree(tmp_path)
    doc = _write(
        tmp_path / "docs/local_llm_solver_orchestration_operator_guide/selected-next-lane.md",
        "## Prior selected next action preserved\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-PRIOR-001\n\n"
        "## Blocker fallback lane\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-PRIOR-FIX-001\n\n"
        "## Selected next action\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-001\n\n"
        "## Blocker fallback lane\n"
        "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CURRENT-FIX-001\n",
    )

    findings = checker.check_paths([doc.relative_to(tmp_path)], tmp_path)

    assert findings == []


def test_current_repo_local_llm_docs_still_pass() -> None:
    findings = checker.check_paths(checker.iter_scanned_docs())

    assert findings == []
