# Checks Run

Checks are recorded after packet creation. This file does not promote evidence and does not record runtime/provider/API/dashboard behavior.

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-provider-provenance-observability-cost-control`
- `rg "NO_FURTHER_PROVIDER_PROVENANCE_OBSERVABILITY_COST_CONTROL_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-PROVENANCE-OBSERVABILITY-COST-CONTROL-FIX-001|provenance|observability|cost|quota|budget|does not implement|does not call providers" docs/evals/runs/alpha-solver-post-level-3-provider-provenance-observability-cost-control`
- Confirm no runtime/provider/API/dashboard files changed.

## Result summary

Results are reported in the PR and final response from the exact commands run in the working tree.
