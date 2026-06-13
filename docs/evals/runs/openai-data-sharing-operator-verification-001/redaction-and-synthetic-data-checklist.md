# Redaction and synthetic-data checklist

This pre-smoke checklist must pass before the first API call.

| Requirement | Status |
|---|---|
| Prompt contains no secrets. | `pending_operator_verification` |
| Prompt contains no private operator notes. | `pending_operator_verification` |
| Prompt contains no credentials. | `pending_operator_verification` |
| Prompt contains no hidden instructions. | `pending_operator_verification` |
| Prompt contains no raw sensitive evidence. | `pending_operator_verification` |
| Prompt uses synthetic task content. | `pending_operator_verification` |
| Output will be reviewed before being committed. | `pending_operator_verification` |

No prompt may be sent until every applicable row is `operator_verified` or explicitly `not_applicable` with a reason.
