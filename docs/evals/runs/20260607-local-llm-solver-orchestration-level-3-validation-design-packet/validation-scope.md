# Validation Scope

## In scope for a future frozen packet

A future frozen packet may define, without executing unless separately approved:

- the exact local-only operator CLI wrapper invocation shape;
- prompt and test-case IDs;
- expected artifact files and schemas;
- safety flag review requirements;
- status classification expectations;
- scoring dimensions and acceptance gates;
- provenance, redaction, and operator/environment note requirements.

## Subject boundary

The subject under test must remain narrow: local LLM solver orchestration behavior through `python -m alpha.local_llm.operator_cli` and the existing local orchestration path.

## Required preserved controls

Any future frozen packet must preserve:

- local-only execution;
- default-off behavior;
- explicit opt-in;
- loopback-only endpoints;
- finite timeout;
- no hosted fallback;
- no provider fallback;
- no hosted provider keys required or accepted;
- `behavior_evidence=false` unless a later evidence model explicitly changes it;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`.

## Out of scope

This packet is docs-only Level 3 validation design work. It does not execute validation, run local model inference, run Ollama, rerun smoke, call hosted providers, expose or call `/v1/solve`, expose or call dashboards, add provider fallback, add hosted fallback, run benchmarks, perform billing work, change runtime behavior, update Google Sheets or backlog workbooks, or promote evidence. It does not establish production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, or evidence-model promotion. It does not reopen Level 2 controlled usage and does not modify the preserved source artifact.
