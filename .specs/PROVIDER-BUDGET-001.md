# PROVIDER-BUDGET-001 · Post-call Provider Cost Accounting

## Goal

Record a safe, structured provider cost accounting record after each successful explicit FastAPI `/v1/solve` OpenAI provider request.

## Scope

- Applies only to the FastAPI `/v1/solve` path when `MODEL_PROVIDER=openai` explicitly selects the OpenAI provider lane.
- Accounting occurs only after a successful provider result.
- Accounting records are built from already-computed `ProviderResult.usage`, `ProviderResult.cost`, `ProviderResult.retry_count`, and explicit safe request metadata.
- Local/offline mode remains unchanged.
- Default CI remains credential-free and network-free.

## Accounting event

The first accounting event name is:

```text
provider.cost.recorded
```

## Record schema

The first accounting record is allowlist-built and may include only these fields when values are present:

| Field | Source |
| --- | --- |
| `event` | Constant `provider.cost.recorded`. |
| `provider` | `ProviderResult.provider`. |
| `model` | `ProviderResult.model`. |
| `model_set` | Safe request metadata. |
| `route` | Safe request metadata. |
| `request_id` | `ProviderResult.request_id` or safe request metadata. |
| `tenant` | Explicit safe request metadata, if provided. |
| `input_tokens` | `ProviderResult.usage.input_tokens`. |
| `output_tokens` | `ProviderResult.usage.output_tokens`. |
| `total_tokens` | `ProviderResult.usage.total_tokens`. |
| `estimated_cost_usd` | `ProviderResult.cost.estimated_usd`; omitted when unknown. |
| `cost_source` | `ProviderResult.cost.source`, including `unknown`. |
| `retry_count` | `ProviderResult.retry_count`. |
| `budget_status` | Constant `recorded`. |
| `accounting_source` | Constant `service:/v1/solve`. |
| `provider_request_id` | Explicitly allowlisted safe provider metadata, if present. |

Unknown usage and cost values must not be fabricated. `None` values are omitted.

## No-secret rules

Accounting records must never include API keys, authorization headers, bearer tokens, raw prompts, raw system prompts, raw provider request bodies, raw provider response bodies, raw exception strings, tracebacks, raw user query text, raw metadata dumps, billing account identifiers, environment dumps, config dumps, or secret-bearing config values.

The guarantee is allowlist construction, not redaction after capture. Accounting helpers must not inspect raw request/response payloads, spread dataclass `__dict__` values, call `vars()` on provider objects, dump raw metadata, or include exception objects.

## Non-goals and deferrals

This increment is account-only post-call accounting. It does not add hard or soft budget enforcement, warnings, pre-call blocking, preflight estimates, persistent tenant budgets, billing API integration, SAFE-OUT budget behavior, provider fallback behavior, database or disk persistence, dashboards, Prometheus/Grafana/OTel expansion, live OpenAI tests, CLI provider budgeting, portable solver changes, local/offline solver budget changes, model-set pricing changes, or response-shape changes.

Existing provider lifecycle telemetry remains separate. Existing FinOps and budget modules are not wired into the live provider path in this first increment.
