# Provider Observability Rules

## Purpose

These rules define future request tracing and response provenance expectations for provider-related paths. They are docs-only and do not implement logging or tracing.

## Request tracing rules

- Every future provider-related attempt should be reviewable through `request_id`, `trace_id`, provider provenance fields, route decision labels, and stop condition labels.
- Trace identifiers must not embed user content, secrets, provider credentials, billing data, payment data, or private user identifiers.
- A trace should distinguish local-only execution, blocked hosted-provider execution, attempted hosted-provider execution, fallback execution, retry execution, and safe-out execution.
- Trace records should identify whether a provider was not called, blocked before call, called successfully, called with error, retried, or superseded.
- Retry and fallback records should preserve parent-child trace relationships without copying sensitive payloads into metadata.
- Observability records should be reviewable offline when possible and must not require calling providers or running models to establish that the record exists.

## Response provenance rules

- Every future response provenance record should state the response source label and response evidence state.
- A response generated without a provider call should use an explicit local, cached, blocked, or safe-out source label rather than leaving provider provenance ambiguous.
- A response generated after a hosted provider attempt should link to provider provenance and usage accounting state when approved.
- Response provenance must distinguish response existence from response quality, correctness, safety, latency, cost savings, or production readiness.
- Raw response text should not be retained in provenance records unless a later accepted policy allows it.
- Redaction state must be visible to reviewers whenever response content, summaries, or identifiers are retained.

## Error and block observability rules

- Blocked provider paths should record a bounded block reason label, policy reference, and budget or quota state when applicable.
- Provider errors should use bounded error classes and should not store raw provider error payloads if they may contain secrets, prompt text, account details, or private identifiers.
- Budget stops, quota stops, and policy stops should be differentiated so reviewers can understand why a provider path was not used.
- Unknown or missing provider provenance must be treated as a review blocker, not as proof that no provider was called.

## Level 7 control

Level 7 controls whether and how these observability rules are used, amended, superseded, or rejected.
