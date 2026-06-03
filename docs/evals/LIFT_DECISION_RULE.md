# Lift Decision Rule

An internal review **decision aid** that separates expert-interrogation lift from
output polish when comparing plain provider output and Alpha Solver expert-preview
output. It supports `OUTPUT-DIFF-MEASUREMENT-HARDENING-001` and
`DISC-MRG-069`, and is used before the first scored Alpha-vs-plain differentiation
run. It is documentation only and is **not proof** of anything about product
quality.

## Dimension clusters

Scores are 0–3 per `docs/evals/RESPONSE_QUALITY_RUBRIC.md` (unchanged here).

- **Lift cluster** (expert interrogation): `d04_assumptions`,
  `d05_hidden_constraints`, `d06_risk_failure`, `d14_comparative_value`.
- **Polish cluster** (presentation): `d03_structure`, `d10_next_actions`,
  `d12_brevity`.
- The remaining dimensions (`d01_intent`, `d02_direct`, `d07_claim_boundary`,
  `d08_evidence_uncertainty`, `d09_decision`, `d11_specificity`, `d13_safety`) are
  scored and contribute to totals but neither gate lift nor trigger the polish
  guard.

## Subscores

- `lift_subscore_plain` = Σ(plain) over the lift cluster.
- `lift_subscore_alpha` = Σ(alpha) over the lift cluster.
- `lift_delta` = `lift_subscore_alpha - lift_subscore_plain`.
- `polish_subscore_plain` = Σ(plain) over the polish cluster.
- `polish_subscore_alpha` = Σ(alpha) over the polish cluster.
- `polish_delta` = `polish_subscore_alpha - polish_subscore_plain`.
- `total_delta` = Σ(alpha − plain) over all 14 dimensions.

## Rule: when does Alpha earn `lift_qualified = yes`?

All of the following must hold:

1. `lift_delta > 0`; and
2. `lift_delta >= polish_delta` (the win is not polish-dominated); and
3. `material_constraint_verified = yes` — at least one surfaced
   constraint/assumption/risk is real, non-invented, non-trivial, and relevant
   (verified from the paired-output capture / expert envelope); and
4. no disqualifying Alpha defect (for example missing the requested deliverable:
   `d01_intent` or `d02_direct` scored 0).

Otherwise `lift_qualified = no`.

## Polish-only-win guard

If `total_delta > 0` but `lift_delta <= 0` and `polish_delta > 0`, set
`polish_only_flag = yes`. Preserve the raw rubric outcome in `winning_surface` if
needed, but cap `winning_surface_resolved` at `Tie` or `Inconclusive`. A more
organized, better-formatted, or longer answer must not be recorded as an Alpha
win when no expert constraint was surfaced.

## Worked examples

- **Genuine lift.** Alpha surfaces a correct hidden constraint and a real failure
  mode; `lift_delta = +3`, `polish_delta = +1`, `material_constraint_verified = yes`,
  no defect → `lift_qualified = yes`, `polish_only_flag = no`.
- **Polish only.** Alpha is better structured with tidier next actions but adds no
  real constraint; `lift_delta = 0`, `polish_delta = +2`, `total_delta = +2` →
  `lift_qualified = no`, `polish_only_flag = yes`,
  `winning_surface_resolved = Tie`.

## Interpretation limits

`lift_qualified` is a per-comparison review decision aid. One prompt, one family, or
one small run cannot establish broad conclusions; small deltas are inconclusive;
plain wins and ties must be recorded honestly.

## Non-claims

This decision aid is internal review tooling only. It:

- does not validate the MVP;
- does not prove Alpha Solver superiority;
- does not prove answer-quality superiority;
- does not prove production readiness;
- does not prove broad runtime readiness;
- does not prove benchmark success;
- does not prove exact billing accuracy;
- does not prove provider reasoning orchestration.
