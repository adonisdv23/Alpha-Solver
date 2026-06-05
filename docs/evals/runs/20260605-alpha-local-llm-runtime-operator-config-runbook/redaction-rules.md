# Redaction Rules

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

These rules apply to future local LLM runtime smoke artifacts and operator notes. This lane does not capture runtime artifacts and does not import smoke results.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Redact before committing or sharing

Redact or omit:

- provider keys;
- API tokens;
- bearer tokens;
- session cookies;
- private URLs;
- nonpublic endpoints;
- local endpoints when they reveal sensitive hostnames, ports, paths, query strings, or user-specific deployment details;
- private filesystem paths;
- usernames in paths;
- environment dumps;
- shell histories;
- process lists that include secrets or private paths;
- full request or response payloads containing private prompts, private data, credentials, or tokens.

## Local endpoint handling

Loopback examples such as `localhost`, `127.0.0.1`, and `::1` may be referenced when they do not expose private deployment details.

Historical endpoint pattern `http://127.0.0.1:11434/api/chat` is preserved as historical context only. It is not automatic runtime config and must be confirmed against the future implementation.

If a future endpoint includes nonpublic hostnames, private paths, query strings, usernames, passwords, or deployment identifiers, replace it with a neutral pattern such as:

```text
http://127.0.0.1:<redacted-port>/<redacted-path>
```

## Environment handling

Do not commit raw environment dumps. If environment state must be summarized, capture only the specific nonsecret field names needed to establish local mode configuration and replace values with redacted placeholders.

Examples:

```text
LOCAL_LLM_ENDPOINT=<redacted-localhost-or-loopback-endpoint>
LOCAL_LLM_MODEL=<redacted-or-approved-model-name>
LOCAL_LLM_TIMEOUT_SECONDS=<finite-seconds>
LOCAL_LLM_EXPLICIT_OPT_IN=<redacted-value>
```

Implementation-specific names remain `TBD` until the implementation has merged.

## Provider-key expectation

Local mode must not require hosted provider keys under the canonical contract. If a future smoke reveals a provider key requirement, stop and classify the issue as `provider key unexpectedly required` rather than adding keys to artifacts.
