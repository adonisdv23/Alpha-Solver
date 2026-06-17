# Checks Run

| Check | Result |
|-------|--------|
| `git diff --check` | PASS: command exited 0 with no output. |
| `python scripts/check_narrative_claim_safety.py docs/CURRENT_STATE.md docs/EVIDENCE_INDEX.md docs/LANE_REGISTRY.md docs/evals/runs/alpha-solver-local-mvp-manual-review-001/*.md` | PASS: `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001 passed (14 files scanned). This is not a completeness claim.` |
| Source-of-truth consistency check for `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` | PASS: selected next state is present in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, and packet `selected-next-state.md`. |
| Changed-line secret-safety check | PASS: custom changed-line scan returned `PASS no changed-line secret value patterns found`. |
| Packet completeness check | PASS: all required packet files are present. |
