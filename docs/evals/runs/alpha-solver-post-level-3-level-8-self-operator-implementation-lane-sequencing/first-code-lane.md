# First code lane

## Recommended first future code lane

The first future code lane should be a **static test scaffold** lane, after a separate implementation plan packet is accepted. It should not add a runnable Self Operator harness.

## Allowed future intent

A later authorized static-test lane may add tests that assert:

- no provider calls are made by default;
- no hosted fallback is introduced;
- no `/v1/solve` or dashboard behavior changes are introduced;
- local-only artifacts and preflight concepts are represented before execution;
- operator confirmation is required before sensitive or externally visible actions;
- blocked and stopped states fail closed;
- acceptance execution remains separate from implementation scaffolding.

## Why this comes first

Static tests should lead code changes because they define safety and non-action expectations before schemas, preflights, confirmation capture, stop states, or wrappers make future behavior runnable.

## Not started here

This packet does not create, edit, or run tests. It only recommends that tests precede executable scaffolds if Level 8 later authorizes planning and implementation lanes.
