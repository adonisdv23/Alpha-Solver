# Test and Smoke Plan

## Current lane

No runtime smoke is executed in this docs-only lane.

## Required checks for this lane

- confirm `git diff --name-only` includes only the canonical spec, `.specs/INDEX.md`, and this docs package;
- confirm `.specs/INDEX.md` contains `LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`;
- confirm exactly one selected next lane is recorded: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-IMPLEMENTATION-001`;
- confirm no source, test, runtime, provider, or dashboard files changed;
- confirm evidence-boundary language remains narrow.

## Future implementation tests

A future implementation must add focused tests for default-off behavior, explicit opt-in, localhost or loopback endpoint acceptance, non-local endpoint rejection, provider-key independence, finite timeout enforcement, no hosted fallback, fail-closed runtime errors, expert two-pass parsing and gating, normalized output shape, metadata preservation, and `behavior_evidence=false` preservation.
