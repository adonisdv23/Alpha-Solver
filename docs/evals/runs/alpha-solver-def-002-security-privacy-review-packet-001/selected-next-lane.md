# Selected next lane

Selected next lane: `ALPHA-SOLVER-DEF-002-GAP-CLOSURE-PLAN-001`

## Why this lane

The verdict is `DEF_002_REVIEW_CAPTURED_OPEN_GAPS` (see `def-002-verdict.md`).
Open gap-closure findings remain in `risk-register.md` (RR-01, RR-02, RR-03,
RR-05, RR-06, RR-07, RR-08). Per the lane selection rule:

- **If open gaps remain → `ALPHA-SOLVER-DEF-002-GAP-CLOSURE-PLAN-001`.** ← selected
- If only operator acceptance remains → `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001`.
- If complete → `ALPHA-SOLVER-DEF-002-CLOSEOUT-001`.

Because remediation work (not merely acceptance) is required, the gap-closure
plan lane is selected.

## Handoff to the gap-closure lane

Inputs the gap-closure lane should consume from this packet:

- `risk-register.md` — the prioritized open gaps with evidence and severity.
- `accepted-residual-risks.md` — items to route to operator acceptance rather
  than code change.
- `def-002-verdict.md` — the closure-gating preconditions.

Suggested gap-closure ordering (High first): RR-02 (plaintext secrets-at-rest),
RR-03 (default credentials), then RR-01 (CORS), RR-05 (classification
registries), RR-07/RR-08 (supply-chain), RR-06 (dependency-declaration drift).
