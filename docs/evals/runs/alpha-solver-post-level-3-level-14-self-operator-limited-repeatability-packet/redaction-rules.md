# Redaction rules

A future repeatability execution lane must preserve raw artifacts below the fresh
output root and import only reviewed, redacted evidence into the repository.

## Must redact or omit

- credentials;
- secrets;
- API keys;
- bearer tokens;
- cookies;
- session values;
- CSRF tokens;
- provider account identifiers;
- machine-local sensitive paths not needed for review;
- raw environment dumps;
- any unexpected external endpoint identifiers.

## Expected redaction result

Because the selected target is local-only and does not use providers, hosted
models, local models, external APIs, browser automation, deployment, billing, or
credentials or secrets, the expected redaction review result is `pass` with no
sensitive value found.

If sensitive material is found, the future lane must stop with
`blocked_by_redaction_issue` and preserve the stop-state artifact below the raw
output root only.
