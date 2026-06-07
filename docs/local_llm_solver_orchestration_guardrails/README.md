# Local LLM Solver Orchestration Guardrail Runbook

## Lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-001`

## Purpose

This docs-only runbook explains the local LLM solver orchestration checker suite and how operators should respond when the guardrails fail. It is a clean replacement for the polluted PR #392 attempt and is scoped only to runbook documentation under `docs/local_llm_solver_orchestration_guardrails/`.

The suite protects local LLM solver orchestration documentation from path drift, stale packet state, and unsupported evidence claims. It preserves evidence boundaries and does not promote documentation artifacts into behavior evidence.

## Guardrail suite entrypoint

Run the aggregate Makefile target first:

```bash
make check-local-llm-orchestration-guardrails
```

The aggregate target runs all three guardrail checkers:

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

Use the direct checker commands only as fallback or manual alternatives when isolating one failure class.

## Files in this runbook

- [checker-inventory.md](checker-inventory.md) explains each checker and what it protects.
- [how-to-run.md](how-to-run.md) gives the normal command flow and manual fallback commands.
- [failure-triage.md](failure-triage.md) maps failure classes to safe responses.
- [common-fixes.md](common-fixes.md) describes allowed documentation fixes that preserve checker intent.
- [non-actions.md](non-actions.md) records actions this runbook must not take.
- [checks-run.md](checks-run.md) records the validation commands for this docs-only lane.

## Selected next action

`NO_FURTHER_GUARDRAIL_RUNBOOK_LANES_SELECTED`

## Blocker fallback lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001`

## Evidence boundary

This is docs-only guardrail runbook work. It does not start the release-readiness ladder, Level 4, runtime work, provider work, benchmark work, dashboard work, `/v1/solve` work, billing work, or evidence promotion.
