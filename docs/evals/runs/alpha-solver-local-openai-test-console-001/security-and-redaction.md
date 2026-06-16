# Security and redaction

## Secret handling

- No API-key field is provided.
- `OPENAI_API_KEY` is read from the local process environment for OpenAI mode.
- API keys are not stored in repo files.
- API keys are not written to saved artifacts by this lane.
- Result rendering uses sanitized JSON.
- Secret-like result keys are redacted.
- Strings containing provider key or bearer patterns are redacted.

## Local-only restriction

The documented run command binds to `127.0.0.1`. The FastAPI routes also reject non-loopback Host headers.

## Result capture

Saving artifacts from the UI is deferred for this first lane. Operators can copy the rendered sanitized JSON manually if needed. No automatic result file is written by the console.
