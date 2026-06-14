# POST-551-NO-ECHO-WIRING-FIX-001 · Local Alpha No-Echo Wiring Fix

## Purpose

Prevent the local modular/reference Alpha entrypoint from returning the exact user prompt as the user-visible `solution` / `final_answer` when deterministic Tree-of-Thought selects the root prompt as its best answer.

## Scope

- Applies only to the local `alpha_solver_entry._tree_of_thought` path through `alpha.solver.observability.AlphaSolver.solve`.
- Adds a narrow no-provider post-SAFE-OUT guard that detects exact normalized prompt echo.
- Replaces supported exact prompt echoes with bounded deterministic local derived answers.
- Replaces unsupported exact prompt echoes with a SAFE-OUT-style unsupported-local clarification that does not pretend to answer the request.
- Preserves existing SAFE-OUT routing, provider-disabled behavior, `/v1/solve` exposure boundaries, hosted-provider boundaries, and local LLM orchestration boundaries.

## Non-goals

- No hosted provider calls, tokens, credentials, or live-provider validation.
- No broad Tree-of-Thought scoring rewrite.
- No production-readiness, value-proof, benchmark-success, provider-validation, or Alpha-superiority claim.
- No public API exposure change.

## Acceptance

- Synthetic no-provider fixtures distinguish exact prompt echo from derived output for supported fixtures.
- Unsupported exact prompt echoes do not receive generic canned answers.
- `solution` and `final_answer` are non-empty, matching derived answer aliases.
- Diagnostics retain the raw echoed ToT answer and mark `echo_detected`.
- Existing focused ToT behavior tests remain compatible.
