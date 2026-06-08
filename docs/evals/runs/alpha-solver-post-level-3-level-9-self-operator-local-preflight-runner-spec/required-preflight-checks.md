# Required preflight checks

Allowed future preflight checks may include:

- Local repo status.
- Branch name.
- Changed-file scope.
- Required docs existence.
- Checker availability.
- Python availability.
- Local command dry-run validation.

Each check must be local-only and must fail closed if it cannot prove safety.
