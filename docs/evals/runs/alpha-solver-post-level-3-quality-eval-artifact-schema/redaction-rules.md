# Redaction Rules

## Purpose

Future quality eval packets may contain sensitive information. Redaction rules protect sensitive content while preserving auditability and raw-output integrity.

## Sensitive information categories

Future packets must identify and protect:

- API keys, access tokens, cookies, session IDs, SSH keys, and credentials.
- Personal data, private emails, phone numbers, addresses, or account identifiers.
- Provider billing details, invoices, payment data, and quota identifiers.
- Proprietary prompts, hidden system prompts, confidential datasets, and private eval inputs when restricted.
- Internal network names, hostnames, local file paths, or secrets that create operational risk.

## Redaction rules

- Do not mutate raw outputs to redact them in place.
- Create a redacted derivative with a separate path and artifact ID.
- Record every redaction in `redaction-log.md` with source path, redacted path, redaction category, reason code, reviewer role, and timestamp.
- Replace sensitive text with stable placeholders such as `[REDACTED_API_KEY_001]` rather than ambiguous deletion.
- Preserve enough surrounding context for review without exposing the sensitive value.
- If raw retention is not allowed, record a deletion or restricted-retention marker approved by the required role.
- Final decision files must state whether they rely on raw outputs, redacted derivatives, or restricted raw outputs.

## Redaction claim boundary

A redacted derivative supports review convenience only. It does not prove the unredacted raw output was unchanged unless linked to a preservation record, hash, and Level 5-approved retention decision.
