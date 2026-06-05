# Failure Troubleshooting Guide

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

This guide is docs-only preparation for future runtime smoke triage. It is not runtime evidence and does not prove any implementation behavior.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Failure categories

### Implementation missing

Use this category when the runtime implementation PR has not merged, the local provider mode cannot be selected, or the implementation-dependent fields are still unknown.

Expected operator action: stop. Do not run smoke. Keep fields marked `TBD`.

### Local service unavailable

Use this category when the local runtime service is not installed, not started, not listening, or refuses local connections.

Expected operator action: stop and record the bounded local failure in future artifacts. Do not fall back to hosted providers.

### Model unavailable

Use this category when the configured local model name is missing, misspelled, not loaded, or otherwise unavailable.

Expected operator action: stop or record a local failure. Do not download or switch models unless the future smoke lane explicitly authorizes that operator action.

### Endpoint not local

Use this category when the endpoint is remote, hosted, LAN, private-network, malformed, ambiguous, unsupported, missing a host, includes userinfo, or does not parse as localhost or loopback.

Expected operator action: stop. Local mode must accept only localhost or loopback endpoints.

### Timeout

Use this category when the local call exceeds the configured finite timeout or the timeout configuration is invalid, missing, or unbounded.

Expected operator action: record timeout as a bounded local failure. Do not silently retry through a hosted provider.

### Malformed response

Use this category when the local runtime returns a response that cannot be parsed into the expected implementation-specific shape.

Expected operator action: record malformed response as a local failure and preserve redacted artifacts.

### Empty output

Use this category when the local runtime returns no usable content.

Expected operator action: record empty output as a local failure and do not label it successful behavior.

### Prompt echo

Use this category when the output appears to repeat the user prompt rather than produce an answer.

Expected operator action: record prompt echo as a local failure under the canonical fail-closed expectation.

### System echo

Use this category when the output appears to expose or repeat system, developer, routing, or hidden instruction content.

Expected operator action: record system echo as a local failure and preserve only redacted artifacts.

### Hosted fallback detected

Use this category when output, logs, metadata, billing traces, provider labels, or network behavior indicate a hosted provider was called or hosted output replaced the local failure.

Expected operator action: stop. Silent hosted fallback from local mode is prohibited unless a later spec explicitly authorizes it.

### Provider key unexpectedly required

Use this category when local mode refuses to run unless a hosted provider key, token, or credential is present.

Expected operator action: stop. Do not add provider keys. Record the issue as a configuration or implementation blocker.

## Non-claim reminder

Troubleshooting notes do not establish runtime readiness, local model quality, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
