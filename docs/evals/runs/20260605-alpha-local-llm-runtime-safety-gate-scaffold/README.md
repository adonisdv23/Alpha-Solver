# Alpha Local LLM Runtime Safety-Gate Scaffold

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

Status: docs-only runtime safety-gate scaffold.

## Purpose

This packet defines guardrails that any future local LLM runtime integration implementation must satisfy before it can make runtime-readiness claims.

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Scope

Allowed scope for this packet is limited to docs under this directory. This packet does not edit source code, test code, runtime routing, provider behavior, `/v1/solve`, dashboard preview behavior, or model execution paths.

## Required safety gates

Future local LLM runtime integration work must satisfy the safety gates summarized in `safety-gate-summary.md`, including default-off operation, explicit opt-in configuration, localhost / loopback endpoint restrictions, no provider keys for local LLM mode, no hosted provider fallback unless separately authorized, finite timeout, fail-closed handling, runtime smoke before readiness claims, and preservation of `behavior_evidence=false` until a later lane explicitly changes the evidence model.

## Packet files

- `README.md`
- `safety-gate-summary.md`
- `local-only-endpoint-guardrails.md`
- `default-off-and-opt-in-requirements.md`
- `fallback-policy-constraints.md`
- `timeout-and-fail-closed-requirements.md`
- `runtime-smoke-gate.md`
- `implementation-review-checklist.md`
- `evidence-boundary.md`
- `selected-next-lane.md`

## Selected next lane

Exactly one selected next lane is recorded:

`ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

This selection is conditional on the separately running runtime-planning PR also selecting or permitting spec work. This scaffold does not override that runtime-planning PR.
