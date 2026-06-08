# Environment Variable Rules

## Environment variable names

Future Level 7-approved work may define environment variable names for provider orchestration only through an authorized spec or implementation lane. Variable names should describe purpose without embedding provider secrets or credential values.

## Environment variable values

- Environment variable values that contain API keys, tokens, credentials, or secret references must be treated as secret material.
- Future tooling must not print full values to stdout, stderr, logs, dashboards, packet captures, or evidence artifacts.
- Future diagnostics should report presence, absence, source category, or validation state without exposing values.
- Any validation of environment variable values is implementation work and is outside this docs-only packet.

## Local files and examples

- Do not commit `.env` files with credentials.
- Do not add realistic key-shaped sample values.
- Do not instruct operators to paste secrets into docs, run packets, shell transcripts, screenshots, or PR descriptions.
- If future Level 7 work needs examples, examples should use clearly non-secret labels rather than provider-shaped key material.

## Non-implementation status

This packet does not configure environment variables, does not validate environment variable values, does not call providers, and does not modify environment checking scripts.
