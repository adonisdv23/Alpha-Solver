# Local-Only Execution Boundary

## Allowed future local work

A future local run harness may only perform work that is explicitly authorized by a later local-only implementation lane and remains inside the local repository or local filesystem scope. Allowed categories are limited to:

- Bounded local preflight checks.
- Local artifact capture.
- Local documentation commands.
- Local checker commands.
- Future local-only tasks explicitly authorized by a later lane.

## Required execution controls

A future local harness should require:

- A declared task identifier.
- A declared local working directory.
- A declared command allowlist.
- A declared artifact directory.
- A declared stop-state policy.
- Human-readable logs for each local command.
- No automatic retry that changes scope or behavior.

## External boundary

The local harness must not cross the local-only boundary. It must not call providers, call hosted models, call external APIs, run local models, use credentials, incur billing, expose dashboard routes, expose or call `/v1/solve`, automate browsers, deploy, add fallback, or promote evidence.

A future lane may separately design provider-aware behavior, but this local run harness design must not be read as authorizing provider calls.
