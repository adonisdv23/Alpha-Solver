# Stop and Blocked States

## Stop states

The lifecycle stop states are `blocked`, `stopped`, `completed`, `failed`, and `archived`.

## `blocked`

`blocked` is the default recoverable fail-closed state. The lifecycle must enter `blocked` for:

- Missing permission.
- Missing evidence.
- Unclear scope.
- Missing credentials boundary.
- Missing fallback boundary.
- Unsafe claims.
- Stale or ambiguous operator approval.
- Any requested action that exceeds the approved local-only boundary.

## `stopped`

`stopped` records intentional cancellation or halt. It prevents automatic resumption and requires either archival or a separate future approved lane to restart safely.

## `completed`

`completed` records in-bound local-only completion. It is not an approval to deploy, publish, call providers, or promote evidence.

## `failed`

`failed` records non-recoverable execution or safety failure. It requires audit evidence, error classification, and prevention of automatic retry.

## `archived`

`archived` is the final preservation state. Archived records are retained for audit and must not be mutated into active lifecycle records.
