# Smoke Authorization Decision

## Decision

Bounded manual local runtime smoke is authorized as the next lane.

Authorized next lane is recorded in `selected-next-lane.md`.

## Basis for authorization

Authorization is based on docs-only review of the canonical spec, implementation surface, config/env surface, endpoint locality checks, fail-closed behavior, redirect handling, focused tests, known full-suite failures, operator runbook, and smoke packet scaffold.

Clean-enough findings:

- Implementation satisfies the canonical optional/default-off local LLM runtime contract.
- Explicit opt-in is required.
- Endpoint locality is loopback-only and fail-closed.
- Provider keys are rejected for local LLM mode.
- Silent hosted fallback is prohibited and not implemented in the reviewed path.
- Redirects are not followed and fail closed.
- `behavior_evidence=false` remains preserved.
- Local provenance is distinguishable from hosted provider output.
- `/v1/solve` and dashboard preview remain blocked.
- Focused local LLM/config tests passed with injected fakes only.
- Full-suite failures are unrelated/pre-existing and do not hide a local LLM blocker.
- Operator runbook and smoke scaffold are sufficient for a future bounded manual smoke lane.

## Authorization limits

This authorization allows only a future bounded manual smoke execution lane. It does not authorize source changes, test changes, hosted provider calls, provider keys, `/v1/solve` exposure, dashboard exposure, smoke result import in this lane, local model quality claims, readiness claims, production claims, benchmark claims, MVP validation claims, provider-orchestration claims, billing claims, or Alpha superiority claims.

## If the next lane discovers a blocker

If the smoke execution lane cannot confirm endpoint locality, exact model name, finite timeout, provider-key absence, explicit opt-in, artifact preservation, or no-hosted-fallback posture, it must stop and classify the outcome as blocked rather than executing smoke.
