# Failure modes

A future preflight runner must stop when:

- Required docs are missing.
- Current branch cannot be confirmed as current-main-based.
- Changed files exceed the allowed scope.
- Required local commands are unavailable.
- Any forbidden command or surface is detected.
- Artifact output would cross the local-only boundary.

Failure must be explicit and reviewable. Silent fallback is forbidden.
