# Checks Run

The following checks are required for this docs-only packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-provider-routing-selection-policy`
- `rg "NO_FURTHER_PROVIDER_ROUTING_SELECTION_POLICY_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-ROUTING-SELECTION-POLICY-FIX-001|routing|selection|capability matching|implicit routing|does not implement|does not call providers" docs/evals/runs/alpha-solver-post-level-3-provider-routing-selection-policy`
- Confirm no runtime/provider/API/dashboard files changed.

Results are recorded in the PR summary rather than as generated logs in this packet.
