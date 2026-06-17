# Security and redaction

## Preserved boundaries

This lane keeps the existing local-only safeguards:

- Loopback Host and peer checks remain on the page and the API route.
- No API key input field is added.
- No result persistence is added.
- No external scripts, styles, fonts, images, telemetry, or remote assets are added.
- The console is not exposed publicly and does not expose `/v1/solve`.
- Smoke-only evidence flags remain set.
- Unsupported-mode requests still fail closed.
- OpenAI mode reads `OPENAI_API_KEY` from the local environment only.

## Redaction

The sanitized result still redacts secret-like fields. Keys matching `api_key`, `authorization`, `bearer`, `access_token`, `refresh_token`, `secret`, and `password` are redacted, and obvious key-marker strings are redacted. Numeric usage token counts under `usage` remain visible because token counts are not secrets.

## What is not claimed

Static checks did not find a known test secret fixture value in the changed files. This is not a security or privacy completion claim. A full security and privacy review remains incomplete and out of scope for this lane.
