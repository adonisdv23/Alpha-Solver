# Scoring Review Authorization Template

Copy and complete this exact authorization before any scoring run:

```text
Operator authorization for blind scoring review:

Scorer: <name or role>
Scope: Score only the 10 cases in the post-579 blind scorer packet for the manual no-provider post-578 pilot.
Scorer packet path: docs/evals/runs/alpha-solver-value-read-blind-scoring-packet-construction-post-579-001/blind-scorer-packet/scorer-packet.md
Score output path: <operator-approved path for locked scores>
No-unblinding boundary: The scorer must not receive, request, infer, reconstruct, or use the unblinding map. No unblinding, final interpretation, provider call, local model call, runtime endpoint, dashboard, public API, Google Sheets mutation, or claim upgrade is authorized.
Stop conditions: Stop if any scorer-facing material leaks response identity; stop if any raw pair is missing; stop if the unblinding map would be committed or disclosed to the scorer; stop if scoring is requested outside the authorized packet or dimensions; stop if unblinding or final interpretation is requested; stop if any provider/local/runtime/dashboard/public API/Google Sheets action is requested.
```
