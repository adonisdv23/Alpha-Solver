# Authorization Boundary

## Authorized in this PR

- Keep a docs-only future smoke-test packet as a blocked draft reference.
- Include command templates with operator-supplied placeholders.
- Include artifact preservation templates.
- Include result import requirements for a later lane.
- Record that endpoint-locality hardening and later explicit operator approval are required before execution.

## Not authorized in this PR

- Running any smoke command.
- Proceeding directly from packet preparation to execution.
- Starting or contacting a local service.
- Calling any local model.
- Calling any hosted service.
- Adding provider access material, private endpoint URLs, or nonpublic network endpoints.
- Changing implementation code, tests, runtime routing, public solve route behavior, dashboard preview behavior, or prior evidence.
- Recording operator-run evidence.
