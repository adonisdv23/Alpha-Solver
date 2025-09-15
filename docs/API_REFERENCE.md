# API Reference

This document lists the public API surface for the Alpha Solver service layer.

- `alpha.executors.math_exec` – local math evaluation helper `evaluate`.
- `service.security` – utilities like `sanitize_query`.
- `service.alerts` – `AlertManager` for latency/budget alerts.
- `service.otel` – tracing helpers `init_tracer`, `span`, `get_exported_spans`.
- `service.logging.redactor` – `redact` strings and mappings with PII removal.
- `service.gating.gates` – routing gate evaluation via `GateConfig` and `evaluate_gates`.
- `service.tenancy.context` – tenant resolution helpers `extract_tenant_id`, `require_tenant_id`.
- `service.mcp.policy_auth` – token providers such as `OAuthClientCredentials`.
- `service.auth.api_keys` – minimal API key management helpers.
