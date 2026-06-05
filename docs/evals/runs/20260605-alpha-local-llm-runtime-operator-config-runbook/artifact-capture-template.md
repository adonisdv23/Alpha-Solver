# Artifact Capture Template

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

This is a placeholder template for a future runtime smoke lane. It is not a smoke result and must not be filled with invented or imported results in this PR.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Future artifact metadata

| Field | Value |
| --- | --- |
| Future smoke lane ID | `TBD` |
| Implementation PR or commit | `TBD` |
| Operator | `TBD-redacted-if-needed` |
| Start timestamp | `TBD` |
| End timestamp | `TBD` |
| Exact command executed | `TBD-redacted` |
| Working directory | `TBD-redacted-private-paths` |
| Exit code | `TBD` |
| Status classification | `TBD` |

## Future runtime configuration capture

| Field | Value |
| --- | --- |
| Local provider mode selected explicitly? | `TBD` |
| Default-off behavior checked? | `TBD` |
| Explicit opt-in field and value | `TBD` |
| Local endpoint field | `TBD` |
| Local endpoint value | `TBD-redacted-or-local-pattern` |
| Endpoint locality confirmed? | `TBD` |
| Local model field | `TBD` |
| Local model name | `TBD` |
| Timeout field | `TBD` |
| Timeout seconds | `TBD` |
| Provider key required? | `TBD-expected-no` |
| Hosted fallback observed? | `TBD-expected-no` |
| `behavior_evidence=false` preserved? | `TBD` |

Historical context only: endpoint pattern `http://127.0.0.1:11434/api/chat`, model `gemma3:4b`, timeout `120`. Confirm against the implementation before use.

## Future output capture

```text
STDOUT:
TBD-redacted
```

```text
STDERR:
TBD-redacted
```

## Future operator notes

- Redactions applied: `TBD`
- Private paths removed: `TBD`
- Provider keys or tokens present before redaction: `TBD-expected-no`
- Nonpublic endpoint details removed: `TBD`
- Evidence boundary acknowledged: `TBD`
- No readiness, validation, superiority, benchmark, production, MVP, runtime, billing, provider-orchestration, or local-model-quality claim made: `TBD`
