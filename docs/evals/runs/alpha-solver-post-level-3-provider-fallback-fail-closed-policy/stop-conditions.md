# Stop Conditions

Fallback policy work or future fallback use must stop when any of the following conditions apply:

- Level 7 has not decided whether and how this packet is used.
- The requested scope would add fallback behavior in a docs-only lane.
- Hosted fallback would be enabled by default.
- Explicit opt-in is missing, stale, ambiguous, revoked, or not reviewable.
- Any blocked fallback state is present.
- Provider calls, model runs, benchmark execution, billing work, `/v1/solve` exposure, runtime changes, provider changes, API changes, dashboard changes, CLI changes, checker changes, test changes, Makefile changes, CI changes, or source-artifact changes would be required.
- The evidence boundary would be weakened or promoted beyond non-promotional local orchestration evidence.
- Audit, redaction, retention, safety, locality, or billing state cannot be proven before execution.

The expected safe outcome after a stop condition is a blocked or fail-closed result with bounded review metadata, not fallback execution.
