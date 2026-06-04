# Blocked Surface Record

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-READINESS-001`

## Surface

`/dashboard/expert-preview` with `MODEL_PROVIDER=local`.

## Reported symptom

A manual local preview attempt appeared to echo the submitted prompt in both the plain provider pane and the Alpha Solver expert preview pane instead of producing substantive answers.

## Evidence handling decision

The attempted local preview output is treated as blocked/invalid for behavior testing if it only echoes prompts or emits placeholder-like deterministic output.

It must not be treated as:

- Alpha pass/fail evidence;
- limited operator-test results;
- scored output;
- benchmark evidence;
- product/runtime readiness evidence;
- Alpha superiority or weakness evidence;
- Batch C readiness evidence; or
- provider behavior evidence.

## Reason

The local supervised preview surface was specified and tested as a no-network UI/local smoke path. The preview route calls the shared service solve function; in local mode the service uses deterministic local `_tree_of_thought` via `alpha_solver_entry` and strips `context.route` before local execution. This does not prove that the expert pane consumes `alpha_solver_portable.py` or the intended limited-operator behavior contract.

## Preservation outcome

No results are imported from the local preview attempt. The attempt is retained only as a surface-readiness blocker indicating that the current local preview should not be used for limited operator behavior testing unless a future lane fixes or proves the intended Alpha behavior surface.
