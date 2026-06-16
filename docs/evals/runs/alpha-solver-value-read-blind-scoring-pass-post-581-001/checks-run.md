# Checks Run

This file records checks run for `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001`.

| Check | Result | Notes |
|-------|--------|-------|
| Live verification: PR #581 merged | pass | GitHub API showed PR #581 closed and merged at `2026-06-15T23:54:37Z`. |
| Live verification: selected next state before edits | pass | `docs/CURRENT_STATE.md` contained `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_SCORING_REVIEW_AUTHORIZATION_POST_BLIND_PACKET_001`. |
| Live verification: scorer packet exists | pass | Authorized scorer packet path exists. |
| Live verification: no open PR | pass | GitHub API returned an empty open-PR list. |
| `git diff --check` | pass | Completed with no whitespace errors. |
| Narrative claim-safety lint on changed markdown files | pass | `python scripts/check_narrative_claim_safety.py` completed for changed markdown files with no findings. |
| Packet consistency checks for this lane folder | pass | Required lane files exist, each authorized case has two score rows, and score-lock metadata is present. |
| Source-identity boundary check over scoring output and log | pass | No source identity, identity map, raw Alpha/baseline identity assignment, unblinding result, or A/B-to-source mapping was exposed. |
| Score-output table consistency check | pass | Every scoring dimension cell, including `Final preference`, uses only `0`, `1`, `2`, `3`, `4`, `5`, or `N/A`; preference labels are stored in the separate `Preference label` column. |
