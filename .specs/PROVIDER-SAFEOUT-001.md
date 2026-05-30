# PROVIDER-SAFEOUT-001 · Structured Provider SAFE-OUT Responses

## Goal

Normalize the explicit FastAPI `/v1/solve` OpenAI provider failure response into a reusable, structured, no-secret provider transport SAFE-OUT envelope.

## Scope

This spec applies only to `/v1/solve` when `MODEL_PROVIDER=openai` routes through the OpenAI provider path and that provider path fails. It does not apply to local/offline solver responses, CLI behavior, portable solver behavior, or reasoning-layer SAFE-OUT logic.

## Response schema

Provider failures return the existing HTTP response status mapping and a lean allowlisted JSON body:

```json
{
  "final_answer": "SAFE-OUT: <safe_message>",
  "safe_out": true,
  "error": {
    "provider": "<provider>",
    "category": "<category>",
    "retryable": true,
    "request_id": "<request-id-or-null>",
    "retry_count": 0,
    "status_code": 503
  }
}
```

`final_answer` keeps the existing `SAFE-OUT: ` prefix. The legacy `error.provider`, `error.category`, and `error.retryable` fields remain present. `error.request_id`, `error.retry_count`, and `error.status_code` are safe correlation fields; `status_code` is copied from `ProviderError.status_code` when available and is `null` when absent.

## Non-goals and invariants

- Does not execute local fallback or automatic fallback.
- Does not add opt-in fallback settings.
- Does not emit `provider.fallback.local` or any fallback telemetry.
- Does not add `fallback_attempted`, `fallback_used`, `fallback_reason`, `provider_failure`, `telemetry_events`, `accounting_recorded`, or `provider.safeout.returned` fields.
- Does not change local/offline defaults.
- Does not change the HTTP status mapping.
- Does not change provider lifecycle telemetry semantics.
- Does not change post-call accounting semantics.
- Does not record cost accounting on provider failure.
- Does not change budget enforcement or budget-exceeded behavior.
- Does not modify CLI, portable solver, or reasoning-layer SAFE-OUT behavior.
- Does not add live OpenAI tests or default network-dependent tests.

## No-secret guarantee

Provider SAFE-OUT response bodies are allowlist-built. They must not include API keys, `OPENAI_API_KEY` values, authorization headers, bearer tokens, raw prompts, raw system prompts, raw user query text, provider request bodies, provider response bodies, raw OpenAI error bodies, raw exception strings, tracebacks, raw metadata dumps, environment dumps, config dumps, or secret-bearing values.

## Tests

Tests use fake or mocked providers only. They must not require a real API key or network access. Coverage includes the unchanged status map, lean response schema, explicit `null` safe correlation fields, no-secret/no-raw-payload safeguards, provider timeout/failure telemetry behavior, unknown exception normalization, success-only accounting, local/offline no-`safe_out` behavior, and absence of fallback telemetry.
