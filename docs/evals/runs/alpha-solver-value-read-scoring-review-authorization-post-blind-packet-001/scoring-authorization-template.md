# Scoring Authorization Template

Copy, complete, and approve this exact authorization text only when the operator intends to authorize scoring. Do not use this template to authorize unblinding, final interpretation, provider calls, local model calls, runtime actions, dashboard/public API exposure, `/v1/solve`, Google Sheets mutation, or product-code changes.

## Required future operator text

I authorize a scoring-only review for `ALPHA-SOLVER-VALUE-READ-SCORING-REVIEW-AUTHORIZATION-POST-BLIND-PACKET-001` under the following boundaries:

- Scorer type: `[human | model-assisted | other explicit type]`
- Scorer identity or tool: `[name, role, tool, or exact model/tool identifier]`
- Scoring packet path: `docs/evals/runs/alpha-solver-value-read-blind-scoring-packet-construction-post-579-001/blind-scorer-packet/scorer-packet.md`
- Score output path: `[exact future score output path; must not be blank]`
- No-unblinding boundary: The scorer must not access, request, infer, reconstruct, or use any identity map or source identity.
- Score lock rule: All case-level scores, notes, contested-score flags, scorer identity, scoring method, and scoring timestamp must be locked in the authorized score output path before any future unblinding request. Scores must not be changed after unblinding.
- Stop conditions: Stop if scorer type, scorer identity/tool, scoring packet path, or score output path is ambiguous or missing; stop if unblinding or final interpretation is requested; stop if provider, local model, runtime, dashboard, public API, `/v1/solve`, Google Sheets, dependency, routing, council, or benchmark action is requested without explicit separate authorization.

I understand this authorization is for scoring only. It does not authorize unblinding, final interpretation, provider calls, local model calls, runtime behavior, dashboard or public API exposure, `/v1/solve`, Google Sheets mutation, dependencies, routing, council behavior, benchmark behavior, or any readiness/value/provider/local-model/security/privacy/production/public/partnership/Pi.dev/Alpha-superiority claim.
