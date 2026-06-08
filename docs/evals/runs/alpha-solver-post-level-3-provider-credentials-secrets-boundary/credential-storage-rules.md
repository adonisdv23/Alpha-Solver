# Credential Storage Rules

## Rules for future work

- Do not store API keys, tokens, service account material, or hosted-provider credentials in repository files.
- Do not add placeholder values that resemble real secrets, test keys, bearer tokens, private keys, or provider-specific credential formats.
- Do not store credentials in docs, source artifacts, run packets, benchmark outputs, screenshots, dashboard snapshots, logs, or captured terminal output.
- Prefer secret references over secret values when future Level 7-approved work needs to document a binding.
- Treat any credential rotation, revocation, validation, or migration as separate Level 7-controlled implementation work.

## Allowed documentation vocabulary

Future docs may name generic concepts such as `API key`, `token`, `secret reference`, `environment variable name`, or `managed secret reference`. They must not include real credential values or realistic key-shaped examples.

## Disallowed storage patterns

- Inline credentials in source or docs.
- Committed `.env` files containing secrets.
- Hard-coded provider tokens in tests, fixtures, examples, or generated artifacts.
- Credential values in issue notes, PR bodies, check logs, or evidence packets.
- Secret payloads copied from hosted secret managers into local packet files.

## Non-implementation status

This document does not create, request, store, rotate, expose, validate, or configure credentials.
