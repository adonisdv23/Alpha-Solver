# Endpoint Validation Rules

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

## Allowed endpoints

Allowed endpoints must use an HTTP-family scheme and a loopback hostname.

Examples covered by offline tests:

- `http://127.0.0.1:11434/api/chat`
- `http://localhost:11434/api/chat`
- `http://[::1]:11434/api/chat`

## Rejected endpoints

Rejected endpoints fail closed before transport invocation with:

`endpoint_not_local_non_evidence`

Examples covered by offline tests:

- `https://example.com/api/chat`
- `http://example.com/api/chat`
- `https://api.openai.com/v1/chat/completions`
- `http://192.168.1.25:11434/api/chat`
- `ftp://127.0.0.1:11434/api/chat`
- `http:///api/chat`
- `http://127.0.0.1:bad/api/chat` (loopback host with invalid port)
- `http://localhost:bad/api/chat` (loopback host with invalid port)
- `http://[::1]:bad/api/chat` (loopback host with invalid port)
- `http://127.0.0.1:99999/api/chat` (loopback host with out-of-range port)
- empty endpoint string

A loopback hostname with a malformed or out-of-range port still fails closed: `urlsplit()` defers port validation, so the validator forces a `parsed.port` read and rejects the endpoint before transport invocation.

## Boundary

This validation only proves endpoint-locality enforcement in the offline adapter seam. It does not prove local model behavior, Ollama service behavior, runtime readiness, or provider orchestration.
