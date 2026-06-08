# Redaction markers

Future artifacts should use explicit placeholders for blocked or redacted values:

- `<REDACTED_SECRET>`
- `<REDACTED_CREDENTIAL>`
- `<BLOCKED_PROVIDER_OUTPUT>`
- `<BLOCKED_EXTERNAL_API_RESPONSE>`
- `<BLOCKED_BILLING_DATA>`
- `<BLOCKED_BROWSER_DATA>`
- `<BLOCKED_DEPLOYMENT_OUTPUT>`
- `<UNPROMOTED_LOCAL_ARTIFACT>`

These markers signal that prohibited content must not be persisted.
