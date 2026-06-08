# Checks Run

This file records checks for the docs-only product-surface dashboard design packet.

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-product-surface-dashboard-design`
- `rg "NO_FURTHER_PRODUCT_SURFACE_DASHBOARD_DESIGN_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-PRODUCT-SURFACE-DASHBOARD-DESIGN-FIX-001|dashboard|does not create|does not expose|operator controls|audit" docs/evals/runs/alpha-solver-post-level-3-product-surface-dashboard-design`
- Confirm no runtime/provider/dashboard/API files changed.

## Boundary of checks

These checks are documentation and static checker commands only. They do not run local model inference, start Ollama, rerun validation, rerun smoke, call hosted providers, expose `/v1/solve`, expose dashboard routes, add provider fallback, add hosted fallback, run benchmarks, score outputs, perform billing work, update Google Sheets or backlog workbooks, or promote evidence.
