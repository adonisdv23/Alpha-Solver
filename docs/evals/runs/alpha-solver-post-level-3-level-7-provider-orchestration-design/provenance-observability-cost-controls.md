# Provenance, Observability, Usage, Cost, and Quota Controls

## Provenance requirements

Future provider-backed behavior must record safe provenance for every provider selection and provider attempt. Required provenance includes provider identifier, model or model-set identifier, route class, enabled/disabled decision, selection reason, fallback attempt number if any, request correlation identifier, policy version where applicable, safety-gate result, and evidence-boundary label.

Raw prompts, raw provider request bodies, raw provider response bodies, raw exception strings, tracebacks, secrets, environment dumps, and unbounded metadata must not be included in provenance records.

## Observability requirements

Future observability must include allowlisted events for provider selection, provider attempt started, provider attempt completed, provider attempt failed closed, fallback considered, fallback skipped, fallback executed, circuit-breaker opened/closed, quota state, cost state, and safety-gate result. Events must be structured, bounded, and safe for logs, traces, metrics, and audit review.

## Usage and cost controls

Future provider orchestration must capture usage and estimated cost only from trusted provider result fields or approved estimation logic. Unknown values must remain unknown. Cost records must be allowlist-built and must not inspect raw provider objects or dump arbitrary metadata.

## Quota controls

Future provider orchestration must define per-provider, per-model-set, per-tenant, and per-environment quota states where applicable. Quota exhaustion must make the provider ineligible or fail closed according to policy. Quota controls must not trigger silent provider fallback unless explicit fallback policy has been accepted.

## Evidence boundary

Observability, usage, cost, and quota records are operational data. They do not by themselves establish quality, benchmark, MVP, production, billing-completeness, provider-readiness, or Alpha-superiority claims.
