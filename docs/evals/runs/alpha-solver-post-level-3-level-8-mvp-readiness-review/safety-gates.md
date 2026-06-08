# Safety Gates

Future planning and implementation lanes must preserve these safety gates:

- Default local-only execution.
- Default operator supervision.
- Stop-before-start preflights.
- Explicit human approval controls.
- No provider calls.
- No hosted model calls.
- No browser control.
- No deployment.
- No billing or cost-incurring behavior.
- No autonomous merge.
- No credential or secret configuration.
- No public API or dashboard exposure.
- No evidence promotion without accepted evidence.

A later lane must stop if any safety gate becomes ambiguous, stale, contradicted, or unenforceable.
