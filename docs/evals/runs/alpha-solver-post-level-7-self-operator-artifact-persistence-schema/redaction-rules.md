# Redaction Rules

## Purpose

Future Self Operator artifacts should preserve raw evidence locally whenever safe. When sensitive values must be removed, redactions must be explicit, minimal, and auditable.

## Required redaction markers

Use bracketed markers that identify the redaction category without exposing the sensitive value:

- `[REDACTED_SECRET]`
- `[REDACTED_API_KEY]`
- `[REDACTED_TOKEN]`
- `[REDACTED_PASSWORD]`
- `[REDACTED_PERSONAL_DATA]`
- `[REDACTED_EMAIL]`
- `[REDACTED_PHONE]`
- `[REDACTED_LOCAL_PATH_SENSITIVE]`
- `[REDACTED_ORG_PRIVATE_DATA]`
- `[REDACTED_SECURITY_SENSITIVE]`

## Redaction ledger fields

Every redaction should be recorded with:

- `redaction_id`;
- `artifact_path`;
- `field_or_line_reference`;
- `redaction_marker`;
- `reason_category`;
- `redacted_by`;
- `redacted_at_utc` or `UNKNOWN_NOT_RECORDED`;
- `raw_value_preserved_elsewhere`: `false` unless a separately approved secure store exists.

## Redaction constraints

- Do not silently delete sensitive spans.
- Do not replace sensitive values with vague prose such as "removed".
- Do not redact more context than necessary.
- Do not mutate source evidence except for the minimal marker substitution required for safety.
- Do not claim unredacted evidence exists unless its location and access policy are documented in an approved secure evidence process.
