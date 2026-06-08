# Provider and external API gates

Static tests must fail with:

- `SELF_OPERATOR_PROVIDER_CALL_BLOCKED` for provider clients, hosted model clients, provider routing, or live-provider invocation.
- `SELF_OPERATOR_EXTERNAL_API_BLOCKED` for HTTP clients, remote fetches, webhooks, telemetry uploads, or external API access.

The tests must not perform network calls while detecting these patterns.
