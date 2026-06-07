# Selected Decision

## Selected decision path

`ADD_STABLE_CLI_WRAPPER`

## Decision statement

A future PR should add a stable, local-only operator CLI wrapper for the Level 2 local LLM solver orchestration path. This decision authorizes only the next implementation lane. This packet does not implement the wrapper.

## Rationale

The selected path is warranted because:

1. PR #368's operator guide selected this decision lane after recording that the repository has a Python/module entry point but no stable operator-facing CLI wrapper.
2. The current module function already centralizes the approved non-production local orchestration behavior and preserves fail-closed local runtime boundaries.
3. Level 2 operators need a repeatable command-oriented surface with stable JSON output and explicit safety configuration.
4. A CLI wrapper can improve usability without broadening exposure if it delegates to the existing module entry point and refuses to add production, dashboard, hosted fallback, or evidence-promotion behavior.

## Current entrypoint status

`MODULE_ENTRYPOINT_ONLY`

The current function remains the source implementation surface until a later implementation lane adds a wrapper. The future wrapper should be a thin operator surface over that function, not a new orchestration implementation.
