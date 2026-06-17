# Checks run

All checks were run locally on 2026-06-17 after creating this packet and updating source-of-truth docs.

| Check | Command | Exact result |
|-------|---------|--------------|
| Whitespace / patch check | `git diff --check` | Passed with no output. |
| Narrative claim-safety lint on changed Markdown files | `CHANGED_MD=$( { git diff --name-only -- '*.md'; git ls-files --others --exclude-standard -- '*.md'; } | sort -u ); python scripts/check_narrative_claim_safety.py $CHANGED_MD` | `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001 passed (13 files scanned). This is not a completeness claim.` |
| Source-of-truth consistency check | Inline Python assertion for `ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001` and `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md` | `source-of-truth consistency check passed for OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Changed-line secret-safety check | Inline Python regex scan of `git diff --unified=0` for common API key / private-key patterns | `changed-line secret-safety check passed` |
| Packet completeness check | Inline Python assertion for required files under `docs/evals/runs/alpha-solver-mvp-cutover-review-001/` | `packet completeness check passed: README.md, live-verification.md, mvp-candidate-checklist.md, blocking-gaps.md, manual-review-plan.md, non-actions.md, non-claims.md, checks-run.md, selected-next-state.md, selected-next-action.md` |
