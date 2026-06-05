# Scorer-Facing Sanitization Template

Lane ID: `ALPHA-BATCH-C-RESULTS-IMPORT-SCAFFOLD-001`

## Purpose

This template creates public scorer-facing entries from preserved raw artifacts. It must not replace the private raw capture record.

## Sanitization requirements

Before a public scorer-facing entry is created, remove or replace:

- private URLs;
- private transcript text beyond minimal necessary excerpts;
- provider identifiers;
- private endpoints;
- keys, secrets, tokens, credentials, account IDs, and billing identifiers;
- operator-only notes;
- any nonpublic assignment map or planning-ledger detail.

## Per-task sanitized entry

### Task ID

`BC-___`

### Prompt summary

`TBD; summarize the prompt without adding sensitive details.`

### Sanitized output summary

`TBD; summarize observable output shape and relevant wording issues without full private transcript text.`

### Minimal excerpt, if needed

```text
TBD; include only a short sanitized excerpt if required for scoring.
```

### Redactions applied

- `TBD`

### Scorer notes

- Direct answer first: `yes / no / unclear`
- Output-format contamination: `yes / no / unclear`
- Claim-boundary issue: `yes / no / unclear`
- Stop condition issue: `yes / no / not applicable / unclear`
