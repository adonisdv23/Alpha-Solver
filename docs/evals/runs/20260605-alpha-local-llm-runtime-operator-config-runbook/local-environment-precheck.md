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
# Confirm the endpoint is an unambiguous HTTP localhost or loopback URL before runtime smoke.
python - <<'PY'
from ipaddress import ip_address
from urllib.parse import urlsplit

endpoint = "TBD"

try:
    parsed = urlsplit(endpoint)

    if parsed.scheme != "http":
        raise ValueError("local LLM endpoints must use the http scheme")

    if not parsed.netloc or parsed.hostname is None:
        raise ValueError("local LLM endpoint must include an unambiguous host")

    if parsed.username is not None or parsed.password is not None:
        raise ValueError("local LLM endpoint must not include username/password/userinfo")

    # Accessing parsed.port forces urllib to reject invalid and out-of-range ports.
    port = parsed.port
    effective_port = port if port is not None else 80

    hostname = parsed.hostname
    is_allowed_name = hostname == "localhost"
    try:
        is_loopback_ip = ip_address(hostname).is_loopback
    except ValueError:
        is_loopback_ip = False

    if not (is_allowed_name or is_loopback_ip):
        raise ValueError("local LLM endpoint host must be localhost or a loopback IP")

    if parsed.fragment:
        raise ValueError("local LLM endpoint must not include a fragment")

    print("accepted local endpoint", parsed.scheme, hostname, effective_port, parsed.path)
except ValueError as exc:
    raise SystemExit(f"rejected local LLM endpoint: {exc}")
PY
```

This template must reject malformed, ambiguous, non-HTTP, non-loopback, and userinfo-bearing endpoints before any future runtime smoke. Examples that must be rejected include:

- `ftp://127.0.0.1:11434/api/chat` because the scheme is not `http`;
- `https://127.0.0.1:11434/api/chat` because the scheme is not `http`;
- `http://user:pass@127.0.0.1:11434/api/chat` because userinfo is present;
- hosted URLs such as `http://api.example.com/api/chat`;
- LAN or private-network URLs such as `http://192.168.1.10:11434/api/chat` or `http://10.0.0.5:11434/api/chat`;
- invalid-port URLs such as `http://127.0.0.1:99999/api/chat` or `http://127.0.0.1:notaport/api/chat`.

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
