# Local-Only Endpoint Guardrails

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Endpoint restriction

Future local LLM runtime integration must allow only localhost / loopback endpoints. Acceptable endpoint intent is limited to local machine addresses such as `localhost`, `127.0.0.1`, or equivalent loopback-only forms.

## Required rejection behavior

Future implementation must fail closed before any model call when the configured endpoint is:

- non-local
- malformed
- absent when local LLM mode is explicitly enabled
- ambiguous between local and non-local routing

## No network expansion

This scaffold does not authorize calls to LAN hosts, remote hosts, hosted providers, provider gateways, public inference APIs, or any non-loopback network endpoint.
