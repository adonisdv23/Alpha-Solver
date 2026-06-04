# Redaction Guidance

Standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`

Status: redaction guidance only. This document does not contain real operator-test evidence.

## Redaction principles

Redaction should protect private or sensitive information while preserving the minimum context needed for import review.

Use these principles:

- redact before packaging for import review;
- keep the smallest useful response snippet;
- preserve operator ratings, stop-condition flags, defect taxonomy labels, and uncertainty;
- replace sensitive values with category placeholders, not invented substitutes;
- document each redaction category in a redaction log;
- never keep a secret merely because it appears in a model response or operator note;
- never expose raw provider payloads, operator-only maps, full unredacted transcripts, or private working notes.

## Content that must be redacted

Always redact:

- API keys, tokens, passwords, cookies, credentials, SSH keys, signing secrets, session IDs, and environment values;
- private personal names unless the operator name is approved for inclusion;
- email addresses, phone numbers, addresses, account IDs, customer IDs, private URLs, ticket URLs, and private repository URLs;
- proprietary client names, internal project names, confidential business details, and non-public incident details;
- raw request or response payloads from providers or APIs;
- raw output maps, operator-only maps, blinding maps, and unblinding maps;
- full transcripts when a short snippet is sufficient;
- any information the operator explicitly marked private or not for import.

## Placeholder vocabulary

Use consistent placeholders:

- `[REDACTED_SECRET]`
- `[REDACTED_PRIVATE_PERSON]`
- `[REDACTED_PRIVATE_ORG]`
- `[REDACTED_PRIVATE_URL]`
- `[REDACTED_ACCOUNT_ID]`
- `[REDACTED_EMAIL]`
- `[REDACTED_PHONE]`
- `[REDACTED_ENV_VALUE]`
- `[REDACTED_RAW_PAYLOAD]`
- `[REDACTED_OPERATOR_ONLY_MAP]`
- `[TRIMMED_UNRELATED_TEXT]`

Do not replace a real value with a fake realistic value. For example, use `[REDACTED_EMAIL]`, not `person@example.com`, unless the example is clearly synthetic and not part of an actual result bundle.

## Response snippet redaction workflow

For each response snippet:

1. Confirm the task ID from approved operator notes.
2. Identify the specific feedback, defect, or stop-condition point the snippet supports.
3. Cut unrelated response text before redaction.
4. Redact secrets, private data, raw payloads, and unsupported map content.
5. Confirm the snippet still supports the operator note without overrepresenting the full answer.
6. Label it as `sanitized_response_snippet`, not `transcript`.
7. Add a redaction-log entry for each redaction category.

## Redaction log format

Use one row per redaction event or grouped category:

| task_id | evidence_item | redaction_marker | reason | meaning_preserved_yes_no | reviewer_note |
| --- | --- | --- | --- | --- | --- |
| `<approved-task-id>` | `sanitized_response_snippet` | `[REDACTED_SECRET]` | secret removed | yes | snippet still shows unsupported-claim wording |

Do not include the original redacted value in the log.

## Preserving notes without exposing private data

When operator notes contain sensitive details, preserve the operational meaning:

- Original meaning: the operator saw an answer that invented a private project status.
- Safe packaged note: `The answer appeared to invent status for [REDACTED_PRIVATE_ORG] project; operator marked invented status defect.`

Do not preserve unnecessary private context:

- Unsafe: `The answer said Client A's unreleased project would ship on 2026-07-15.`
- Safe: `The answer stated a specific release status/date for [REDACTED_PRIVATE_ORG] without evidence.`

## Handling missing or unsafe fields

If a field is blank, unsafe, or unverifiable:

- do not fill it from memory;
- do not derive it from snippets;
- do not ask another system to infer it;
- mark it with the applicable missing-field or blocked marker;
- explain the remediation needed if import is blocked.

Examples:

- `operator_rating_brevity_0_3: NOT_PROVIDED`
- `task_id: BLOCKED_UNVERIFIED_TASK_ID`
- `evidence_snippet: REDACTED_RAW_PAYLOAD`
- `bundle_status: blocked until raw payload is removed and replaced with a safe snippet, if available`

## Quality check before import review

Before marking a bundle import-ready, confirm:

- redactions use approved placeholders;
- no placeholder hides a fabricated value;
- snippets remain intelligible after redaction;
- the redaction log does not reveal redacted content;
- private details are not repeated in filenames, headings, comments, metadata, or screenshots;
- no unsupported claim remains in narrative text.
