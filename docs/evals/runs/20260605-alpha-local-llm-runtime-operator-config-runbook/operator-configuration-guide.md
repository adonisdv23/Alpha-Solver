# Operator Configuration Guide

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

This guide is docs-only preparation for a future optional local LLM runtime path. It does not implement configuration, prove configuration behavior, or authorize runtime use.

Runtime implementation may be running separately under `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-IMPLEMENTATION-001`. Until that implementation is merged and reviewed, implementation-dependent field names, environment variables, CLI flags, config keys, and runtime behavior are `TBD`.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Required operator setup concepts

| Setup concept | Implementation field | Required expectation |
| --- | --- | --- |
| Local endpoint | `TBD` | Must point only to localhost or loopback. Non-local endpoints must fail closed. |
| Local model name | `TBD` | Must identify the local model selected by the operator. |
| Timeout seconds | `TBD` | Must be finite and explicitly represented in runtime configuration or invocation. |
| Explicit opt-in | `TBD` | Local LLM runtime mode must not activate unless the operator explicitly opts in. |
| Default-off behavior | `TBD` | Local LLM mode must remain optional and disabled by default. |
| Hosted fallback behavior | `TBD` | Silent hosted fallback from local mode is not expected and must not be assumed. |
| Provider key requirement | `TBD` | Local mode must require no hosted provider key. |

## Historical values preserved for context only

Previous local smoke context used:

- endpoint pattern: `http://127.0.0.1:11434/api/chat`
- model used in smoke: `gemma3:4b`
- timeout used in smoke: `120`

These are not automatic runtime configuration values. They must be confirmed against the future implementation before any operator uses them.

## Configuration expectations

1. Start from the canonical contract in `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.
2. Confirm that the implementation has a documented way to select local provider mode explicitly.
3. Confirm that local provider mode is default-off before operator opt-in.
4. Confirm the exact field names for endpoint, model name, timeout seconds, and opt-in.
5. Confirm that no hosted provider key is required for local mode.
6. Confirm that local failures remain local failures and are not silently replaced with hosted output.
7. Confirm that observability or artifact metadata labels output as local only when it came from the local runtime path.

## Example placeholder record

Do not fill this record with real secrets, private paths, or unredacted endpoints.

| Field | Future value |
| --- | --- |
| Implementation PR merged? | `TBD` |
| Runtime config source reviewed? | `TBD` |
| Local endpoint field name | `TBD` |
| Local endpoint value | `TBD-localhost-or-loopback-only` |
| Local model field name | `TBD` |
| Local model value | `TBD` |
| Timeout field name | `TBD` |
| Timeout value | `TBD-finite-seconds` |
| Explicit opt-in field name | `TBD` |
| Explicit opt-in value | `TBD` |
| Hosted fallback disabled or absent? | `TBD` |
| Provider key required? | `TBD-expected-no` |
