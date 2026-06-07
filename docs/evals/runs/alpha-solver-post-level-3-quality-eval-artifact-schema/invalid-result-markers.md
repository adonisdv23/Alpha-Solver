# Invalid Result Markers

## Purpose

Future eval packets need explicit invalid result states so incomplete or unusable captures remain visible without being promoted as valid evidence.

## Required invalid result states

| Marker | Meaning | Evidence handling |
| --- | --- | --- |
| `VALID_RESULT` | Artifact is valid for its declared purpose. | May be considered by scoring and final decision. |
| `INVALID_MISSING_RAW_OUTPUT` | A derived note or score has no preserved raw output. | Exclude from scoring and final claims. |
| `INVALID_MUTATED_RAW_OUTPUT` | Raw output was edited in place or cannot be verified as unmodified. | Quarantine and exclude unless Level 5 accepts a restricted derivative policy. |
| `INVALID_UNAUTHORIZED_RUN` | Execution occurred without required authorization. | Preserve for audit, exclude from promoted evidence. |
| `INVALID_SCOPE_VIOLATION` | Artifact reflects a forbidden provider, runtime, API, dashboard, billing, or benchmark action. | Preserve for audit and block promotion. |
| `INVALID_REDACTION_GAP` | Sensitive data appears without required redaction or restriction. | Restrict access, create redaction log, block public review. |
| `INVALID_HASH_MISMATCH` | Recorded hash does not match artifact bytes. | Quarantine until resolved. |
| `INCOMPLETE_CAPTURE` | Capture ended early or lacks required stdout, stderr, status, metadata, or command provenance. | Keep visible and mark incomplete. |
| `BLOCKED_BY_ENVIRONMENT` | Environment limitation prevented valid execution or checking. | Keep as blocked evidence, not failure evidence. |
| `SUPERSEDED_BY_RERUN` | Later authorized rerun replaced this result. | Keep in inventory and cite superseding artifact. |
| `REDACTED_DERIVATIVE_ONLY` | Only a redacted derivative can be reviewed under current policy. | Final decision must state raw-source availability limits. |

## Invalid marker rules

- Invalid results must not be deleted solely because they are invalid.
- Invalid markers must be visible in inventory, scoring records, and final decision exclusions.
- A final decision must distinguish invalid, incomplete, blocked, and valid artifacts.
