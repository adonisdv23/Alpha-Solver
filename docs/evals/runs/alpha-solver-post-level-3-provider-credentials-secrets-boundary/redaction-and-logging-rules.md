# Redaction and Logging Rules

## Redaction principles

Future provider orchestration work must redact secrets before any value can reach logs, dashboards, errors, traces, metrics, evidence packets, screenshots, or operator-facing summaries. Redaction must be applied to API keys, tokens, secret references when sensitive, provider request headers, authorization metadata, and any derived credential material.

## Logging restrictions

- Do not log raw credentials, credential substrings, bearer headers, provider tokens, service account payloads, or environment variable values.
- Do not log provider request bodies or response bodies if they may contain credential material.
- Do not use debug logs as an exception to secret redaction.
- Do not add fallback paths that log credentials after a provider error.
- Do not capture credentials in benchmark artifacts, model-run packets, or billing evidence.

## Safe diagnostic shape for future work

Future diagnostics may report non-sensitive states such as `credential reference configured`, `credential reference missing`, `redacted`, or `operator confirmation required`. The diagnostic must avoid secret values and avoid realistic key-shaped examples.

## Non-implementation status

This packet defines redaction and logging restrictions only. It does not implement redaction code, modify logging code, call providers, run models, or generate provider diagnostics.
