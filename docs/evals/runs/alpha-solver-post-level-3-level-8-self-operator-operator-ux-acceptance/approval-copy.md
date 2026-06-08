# Approval Copy

## Required approval request text

The approval request must include copy equivalent to:

> Review this Self Operator task before it runs. Approve only if the task, scope, evidence boundary, artifacts, and stop option match your intent.

## Required fields

- Task name or identifier.
- Requested action.
- Scope summary.
- Evidence sources to use.
- Files, directories, or artifacts expected to be read or created.
- Whether the action is inspect-only or change-producing.
- Stop instruction.
- Provider boundary statement.

## No-provider-call boundary copy

The approval request must include copy equivalent to:

> This approval does not authorize hosted provider calls, billing, credential use, or external model fallback. If provider access is required, stop and route to an explicitly approved provider lane.

## Approval buttons or commands

The operator must have distinct choices equivalent to:

- `Approve this action`
- `Reject / do not run`
- `Stop and mark blocked`

The UX must not use ambiguous approval copy such as `continue` when the next action could make changes, create artifacts, consume credentials, or call providers.
