# Checks Run

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | Listed only the new release-gate checker module, CLI, tests, and docs packet as untracked before staging. |
| `git diff --name-only` | PASS | No tracked-file diff was present before staging because this lane adds new files only. |
| `git diff --check` | PASS | No whitespace errors. |
| `python -m pytest -q tests/test_self_operator_release_gate.py` | PASS | 12 focused tests passed. |
| `python scripts/check_self_operator_release_gate.py --help` | PASS | Help text printed and included the non-readiness claim boundary. |
| `python scripts/check_self_operator_release_gate.py --repo-root . --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-release-gate-checker/current-gate-report.json` | PASS (expected blocked exit) | Wrote deterministic JSON and exited `1` because current final status is `blocked_missing_import`. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-release-gate-checker` | PASS | Packet consistency check passed for this packet. |
| `rg -n "blocked_missing_import\|blocked_missing_interpretation\|blocked_missing_runbook_finalization\|eligible_for_release_closeout_review\|does not claim MVP readiness\|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-LOCAL-ACCEPTANCE-RESULT-IMPORT-001" alpha/self_operator/release_gate.py scripts/check_self_operator_release_gate.py tests/test_self_operator_release_gate.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-release-gate-checker` | PASS | Required final-status, non-readiness, and selected-next-lane markers were present. |
