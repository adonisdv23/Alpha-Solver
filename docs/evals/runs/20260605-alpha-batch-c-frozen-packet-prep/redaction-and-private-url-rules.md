# Redaction and Private URL Rules

Lane ID: `ALPHA-BATCH-C-RESULTS-IMPORT-SCAFFOLD-001`

## Redaction rule

Public docs must not contain sensitive or nonpublic material from a future Batch C run.

## Must remove or replace

- private URLs;
- private transcripts and full raw outputs;
- provider identifiers;
- private endpoints and nonpublic routes;
- keys, secrets, tokens, credentials, account IDs, and billing identifiers;
- operator-only notes;
- private assignment maps;
- nonpublic planning-ledger details;
- any copied content that would identify a private manual context.

## Replacement style

Use bracketed public placeholders such as:

- `[REDACTED PRIVATE URL]`
- `[REDACTED PRIVATE TRANSCRIPT]`
- `[REDACTED PROVIDER IDENTIFIER]`
- `[REDACTED PRIVATE ENDPOINT]`
- `[REDACTED SECRET]`
- `[REDACTED OPERATOR NOTE]`

## Minimum public evidence standard

Public scorer-facing docs may summarize output shape, boundary issues, and short sanitized excerpts only when needed. They must not publish complete private transcripts.

## Redaction log fields

| field | value |
| --- | --- |
| task_id | `BC-___` |
| sensitive category removed | `TBD` |
| replacement placeholder | `TBD` |
| scorer-facing impact | `none / minor / material` |
| reviewer initials | `TBD` |
