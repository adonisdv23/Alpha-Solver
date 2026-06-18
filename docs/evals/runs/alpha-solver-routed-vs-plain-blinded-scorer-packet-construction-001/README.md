# Routed-vs-plain blinded scorer packet construction 001

Lane ID: `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001`

Verdict: `BLINDED_SCORER_PACKET_CONSTRUCTED_REVIEW_ONLY`

This docs-only lane constructs a scorer-facing blinded packet for the previously recorded routed-vs-plain manual output collection. It prepares source-neutral task context, Response A, Response B, blank scoring fields, blank preference fields, blank rationale fields, and caveat fields for `RVP-001` through `RVP-012`.

This lane does not score, unblind, choose winners, compute totals, interpret results, change source outputs, call providers, run hosted models, run local models, execute tools, browse, mutate Google Sheets, add dependencies, expose `/v1/solve`, expose dashboard/public API behavior, deploy, or make readiness, benchmark, quality, production/public, value, security/privacy, autonomous-readiness, or Alpha-superiority claims.

## Packet contents

- `scorer-packet.md` contains the complete scorer-facing packet for all 12 tasks.
- `blinded-tasks/RVP-001.md` through `blinded-tasks/RVP-012.md` contain per-task scorer-facing copies.
- `rubric.md` freezes the 12 route-value dimensions and 0-3 scale.
- `scoring-sheet-template.md` provides blank scoring/preference/rationale/caveat fields only.
- `ab-key-custody.md` documents custody rules without committing the A/B key.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001`
