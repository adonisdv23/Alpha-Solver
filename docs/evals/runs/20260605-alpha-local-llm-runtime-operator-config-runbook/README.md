# Local LLM Runtime Operator Configuration Runbook

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

Status: docs-only operator preparation runbook for the optional local LLM runtime path.

## Purpose

This directory prepares operator-facing documentation for configuring and smoke-testing a future optional local LLM runtime path.

This lane is documentation only. It does not implement runtime integration, does not execute smoke, does not call a local model, does not call a hosted provider, and does not import smoke results.

Runtime implementation may be running separately under `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-IMPLEMENTATION-001`. This runbook does not prove that implementation exists, has merged, works, or is ready for runtime use.

## Canonical contract

The canonical implementation contract is `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

Operators must confirm the eventual implementation against that contract before using these templates as runtime instructions.

## Historical local smoke context only

Prior local smoke materials referenced these historical values:

- endpoint pattern: `http://127.0.0.1:11434/api/chat`
- model used in smoke: `gemma3:4b`
- timeout used in smoke: `120`

These values are historical context only. They are not automatic runtime configuration and must be confirmed against the future implementation before use.

## Runbook contents

- `operator-configuration-guide.md` records operator setup fields and default-off expectations.
- `local-environment-precheck.md` provides future-use local precheck command templates; they were not executed in this lane.
- `runtime-smoke-runbook.md` provides a future-use smoke sequence; it was not executed in this lane.
- `artifact-capture-template.md` provides a placeholder artifact template for future runtime smoke.
- `redaction-rules.md` defines redaction requirements for future artifacts.
- `failure-troubleshooting-guide.md` lists implementation and runtime failure categories.
- `evidence-boundary.md` preserves the narrow documentation-only boundary.
- `runbook-preservation-checklist.md` records preservation checks for this docs-only lane.
- `selected-next-lane.md` records exactly one selected next lane.

## Operator setup fields

Implementation-dependent fields remain `TBD` until the runtime implementation PR has merged and the final configuration interface is known.

| Field | Status for this lane | Notes |
| --- | --- | --- |
| Local endpoint | `TBD` | Must be localhost or loopback only under the canonical contract. Historical context: `http://127.0.0.1:11434/api/chat`. |
| Local model name | `TBD` | Must be confirmed against the future implementation. Historical context: `gemma3:4b`. |
| Timeout seconds | `TBD` | Must be finite. Historical context: `120`. |
| Explicit opt-in flag or setting | `TBD` | Local LLM mode must require explicit operator opt-in. |
| Default-off behavior | Required | Local LLM mode must remain optional and default-off. |
| Hosted fallback | Prohibited unless a later spec explicitly authorizes it | No silent hosted fallback is expected. |
| Provider key requirement | None expected for local mode | Local LLM mode must not require hosted provider keys. |

## Evidence boundary summary

This PR is operator runbook documentation only.

It is not runtime implementation, runtime smoke execution, runtime evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
