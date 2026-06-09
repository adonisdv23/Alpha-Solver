# Checks Run

| Command | Result | Notes |
|---|---|---|
| `git status --short` | Passed | Showed only the new manual local acceptance packet directory as untracked before staging. |
| `git diff --name-only` | Passed | No tracked-file diff before staging; final changed-file scope was rechecked with staged files. |
| `git diff --check` | Passed | No whitespace errors. |
| `make check-local-llm-orchestration-guardrails` | Passed | Evidence-boundary, doc path/link, and packet consistency guardrails passed. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet` | Passed | Packet consistency check passed for the new packet directory. |
| `rg -n "stop if explicit operator confirmation is missing\|run_local_dry_run_wrapper\|DryRunResult\|ready_for_operator_supervised_local_dry_run\|MLA-001\|MLA-010\|NOT RUN\|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-OPERATOR-SUPERVISED-LOCAL-ACCEPTANCE-EXECUTION-001\|does not run acceptance\|does not claim MVP readiness" docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet` | Passed | Required acceptance-preparation tokens were present. |
| `git status --short` | Passed | Fix pass showed only `acceptance-prerequisites.md` and `release-closeout-handoff.md` modified before checks-run was updated. |
| `git diff --name-only` | Passed | Fix pass showed only packet files changed. |
| `git diff --check` | Passed | No whitespace errors in the fix diff. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet` | Passed | Packet consistency check passed for the updated packet directory. |
| `rg -n "final runbook\|runbook reviewed\|runbook finalized\|runbook updated\|MVP/Self Operator runbook\|release closeout remains blocked\|stop if explicit operator confirmation is missing" docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet` | Passed | Required fix tokens were present after restoring runbook gates. |
