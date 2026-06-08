# Source Evidence Reviewed

## Purpose

This file records the local repo evidence reviewed for the docs-only provider routing and selection policy packet.

## Evidence reviewed

- `AGENTS.md` was reviewed for repo-level workflow, validation, source-of-truth, and safety instructions.
- Existing post-Level-3 packets under `docs/evals/runs/alpha-solver-post-level-3-*` were reviewed for packet structure, decision-authority wording, evidence-boundary wording, selected-next-action usage, blocker-fallback-lane usage, and checks-run style.
- Existing local LLM/provider-oriented packets under `docs/evals/runs/20260604-alpha-local-llm-provider-*`, `docs/evals/runs/20260605-alpha-local-llm-provider-*`, and `docs/evals/runs/20260605-alpha-local-llm-solver-orchestration-*` were reviewed as context only.
- `scripts/check_local_llm_packet_consistency.py` was reviewed to keep packet markers, selected-next-action, blocker fallback, and non-actions compatible with repo packet checks.

## Evidence limits

This review was inspect-only. It did not implement routing, does not call providers, does not select providers at runtime, does not add fallback behavior, does not expose `/v1/solve`, does not run models, does not run benchmarks, does not perform billing work, and does not promote evidence.
