# Local LLM Solver Orchestration Surface Audit

## Lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-SURFACE-AUDIT-001`

## Purpose

This docs-only audit maps which built Alpha Solver components are not used by the current local LLM runtime path, which bypassed components could directly improve response quality, and which components should be integrated first in a later explicit implementation lane.

## Prerequisites recorded

- PR #327 is treated as squashed, merged, closed, and recorded in GS per lane instructions.
- The local LLM runtime track is closed with terminal next action `STOP-HERE-LOCAL-LLM-RUNTIME-TRACK-CLOSED`.
- `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-SPEC-001` may be running concurrently and is not modified here.

## Audit outputs

- `current-local-path-trace.md` maps the active local LLM runtime path.
- `unused-built-surface-map.md` classifies bypassed built surfaces.
- `quality-impact-matrix.md` estimates direct response-quality impact for implemented surfaces.
- `integration-risk-matrix.md` records implementation and release risks.
- `recommended-integration-order.md` records the required integration order.
- `non-active-or-stubbed-surfaces.md` records stub, inactive, unknown, and blocked surfaces.
- `source-evidence-ledger.md` names the inspected source files and evidence facts.
- `evidence-boundary.md` preserves the narrow non-claim boundary.
- `audit-preservation-checklist.md` records audit checks.
- `selected-next-lane.md` records exactly one selected next lane.

## Headline conclusion

The current local LLM runtime path is a narrow provider-adapter runtime that validates explicit local configuration, loads the portable contract as prompt source, maps the request to an Ollama-style chat payload, sends only to a loopback/local transport, parses a static chat response, and returns a bounded `LocalLLMAdapterResult` with `behavior_evidence=false`. It intentionally does not invoke the existing solver orchestration surfaces such as expert two-pass, confidence mode gates, SolverEnvelope orchestration, ToT, SAFE-OUT, ReAct-lite, CoT validation, `/v1/solve`, provider/model-set routing, or dashboard preview.

## Selected next lane

See `selected-next-lane.md` for the single recorded next-lane decision.
