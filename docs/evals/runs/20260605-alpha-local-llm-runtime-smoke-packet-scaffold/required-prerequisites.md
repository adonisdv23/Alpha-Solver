# Required Prerequisites

This scaffold is blocked until the prerequisites below are satisfied and recorded by a future lane.

## Already Required Planning Prerequisites

- PR #309 must be squashed, merged, closed, and recorded in GS.
- PR #311 must be squashed, merged, closed, and recorded in GS.
- PR #312 must be squashed, merged, closed, and recorded in GS.

## Future Implementation Prerequisite

- A future implementation PR must create the local LLM runtime integration before smoke is attempted.
- That future implementation PR must be reviewed, squashed, merged, closed, and recorded in GS before smoke execution.
- `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001` may be running separately; this scaffold does not override that spec lane.

## Future Review Gate Prerequisite

- A future review gate must explicitly authorize runtime smoke execution.
- Authorization must be specific to local runtime smoke and must not be inferred from this scaffold.

## Runtime Environment Prerequisites

A future smoke operator must record:

- Localhost or loopback-only endpoint.
- Exact local model name.
- Finite timeout.
- No hosted provider fallback.
- No provider keys for local mode.
- Raw artifact preservation location.
- Sanitized import location after execution.

## Blocked Until Complete

If any prerequisite is missing, the future smoke run must be classified as blocked and must not be executed.
