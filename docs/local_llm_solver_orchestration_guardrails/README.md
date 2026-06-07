# Local LLM Solver Orchestration Guardrail Runbook

## Scope

This runbook is documentation-only guardrail hardening for the local LLM solver orchestration checker suite. It explains what the existing offline checkers protect, how to run them, how to triage failures, and how to fix documentation or packet issues while preserving evidence boundaries.

## Source evidence reviewed

This runbook is based on the accepted repository-local checker and doc artifacts:

- `scripts/check_local_llm_evidence_boundaries.py`
- `scripts/check_local_llm_doc_paths.py`
- `scripts/check_local_llm_packet_consistency.py`
- `tests/test_local_llm_evidence_boundaries.py`
- `tests/test_local_llm_doc_paths.py`
- `tests/test_local_llm_packet_consistency.py`
- `docs/local_llm_solver_orchestration_operator_guide/`
- `docs/evals/runs/local-llm-solver-orchestration-index/`

## Runbook files

- `checker-inventory.md` describes each checker and the boundary it protects.
- `how-to-run.md` lists direct checker commands and the current aggregate Makefile coverage.
- `failure-triage.md` explains how to interpret common failures without weakening evidence boundaries.
- `common-fixes.md` gives safe documentation-only repair patterns.
- `non-actions.md` records actions this runbook does not authorize.
- `checks-run.md` records checks used for this docs-only runbook lane.

## Selected next action

```text
NO_FURTHER_GUARDRAIL_RUNBOOK_LANES_SELECTED
```

## Blocker fallback lane

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001
```

## Evidence boundary

This runbook is not behavior evidence and does not start the roadmap-selected release-readiness ladder track. It is a guide for preserving the already-accepted local-only, non-promotional documentation boundary; it does not promote the Level 2 or Level 3 packets into readiness, quality, benchmark, provider, billing, dashboard, `/v1/solve`, broad-runtime, or evidence-model promotion evidence.
