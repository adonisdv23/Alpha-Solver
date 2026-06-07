# Checks Run

The following checks are required for this docs-only packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-product-surface-operator-controls`
- `rg "NO_FURTHER_PRODUCT_SURFACE_OPERATOR_CONTROLS_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-PRODUCT-SURFACE-OPERATOR-CONTROLS-FIX-001|default-off|explicit enablement|confirmation gates|audit requirements|does not implement" docs/evals/runs/alpha-solver-post-level-3-product-surface-operator-controls`
- Confirm no runtime/provider/dashboard/API files changed.

Results are recorded in the PR summary rather than as generated logs in this packet.
