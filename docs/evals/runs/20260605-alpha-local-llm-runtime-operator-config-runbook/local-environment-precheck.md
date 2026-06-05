# Local Environment Precheck

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

This file is a future-use template only. The commands below were not executed in this lane. This lane does not call a local model, does not call a hosted provider, does not make network calls, and does not run smoke.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Future-use precheck goals

A future operator may use implementation-specific prechecks to confirm:

- a local service is installed and intentionally started;
- the endpoint is localhost or loopback only;
- the intended local model is available;
- the timeout is finite;
- local mode requires explicit opt-in;
- local mode is default-off before opt-in;
- no hosted provider key is required;
- no hosted fallback occurs from local mode.

## Implementation-dependent values

| Value | Future value |
| --- | --- |
| Endpoint field | `TBD` |
| Endpoint value | `TBD` |
| Model field | `TBD` |
| Model value | `TBD` |
| Timeout field | `TBD` |
| Timeout seconds | `TBD` |
| Explicit opt-in field | `TBD` |
| Explicit opt-in value | `TBD` |

Historical context only: endpoint pattern `http://127.0.0.1:11434/api/chat`, model `gemma3:4b`, timeout `120`. These values are not automatic runtime config.

## Future-use command templates, not executed here

Replace placeholders only after the implementation has merged and the exact operator interface is known.

```bash
# Confirm the runtime implementation exposes the expected local LLM config fields.
<TBD-alpha-command-or-doc-command> --help
```

```bash
# Confirm the local service process is intentionally running.
<TBD-local-runtime-status-command>
```

```bash
# Confirm the selected local model is available without downloading during smoke.
<TBD-local-runtime-model-list-command>
```

```bash
# Confirm the endpoint is loopback or localhost before runtime smoke.
python - <<'PY'
from urllib.parse import urlparse
endpoint = "TBD"
parsed = urlparse(endpoint)
print(parsed.scheme, parsed.hostname, parsed.port, parsed.path)
assert parsed.hostname in {"localhost", "127.0.0.1", "::1"}
PY
```

```bash
# Confirm required provider-key variables are not needed for local mode.
<TBD-alpha-local-mode-dry-config-command>
```

```bash
# Confirm default-off behavior before explicit opt-in.
<TBD-alpha-command> <TBD-minimal-input> --expect-local-mode-off
```

## Stop conditions for future operators

Stop before runtime smoke if any of the following are true:

- the runtime implementation has not merged;
- the exact local configuration fields remain unknown;
- the endpoint is not localhost or loopback;
- the service is unavailable;
- the model is unavailable;
- the timeout is missing or unbounded;
- a hosted provider key is required for local mode;
- the system appears to silently fall back to a hosted provider;
- redaction requirements cannot be satisfied.
