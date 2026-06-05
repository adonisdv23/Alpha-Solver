# Planning Scope

This file defines a docs-only planning scaffold. It is not implementation authorization and does not change runtime behavior.

## In scope

- Preserve a narrow planning scaffold for a possible future local LLM runtime integration lane.
- Record prerequisites that must be satisfied before runtime integration can be considered.
- Identify likely future runtime touchpoints without editing them.
- Record risks that a future lane must mitigate if evidence later supports integration work.
- Keep the evidence boundary explicit and narrow.

## Out of scope

- Source code changes.
- Test code changes.
- Runtime routing changes.
- `/v1/solve` changes.
- Dashboard preview changes.
- Provider key handling.
- Live Ollama calls.
- Hosted provider calls.
- Local model calls.
- Network calls.
- Smoke execution.
- Smoke result import.
- Smoke interpretation.
- Batch C work.
- Readiness, validation, superiority, benchmark, billing, provider-orchestration, production, runtime, MVP, or local-LLM-quality claims.

## Smoke status for this lane

No local smoke result has been imported or interpreted in this lane. Any future runtime integration planning remains blocked pending future evidence.
