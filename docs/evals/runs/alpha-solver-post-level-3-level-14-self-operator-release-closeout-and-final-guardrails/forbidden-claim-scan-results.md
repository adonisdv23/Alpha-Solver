# Forbidden-claim scan results

## Exact scan command

Run from the repo root on 2026-06-11, after all of this lane's edits
(including this file and `checks-run.md`):

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs alpha scripts tests
```

Total hits: 4046 matching lines. Baseline on `main` before this
lane's edits: 3989 (the #472 lane's recorded final count); every added line
is inside this lane's new packet directory, the new guardrail test module,
or this packet's scan/check records quoting the patterns.

## Review method (every hit reviewed)

The same three-tier method recorded by the #472 scan was applied, so the
risk-bearing hits got individual reading and the bulk hits got an explicit,
reproducible rule:

1. Claim-type pattern hits (`production ready`, `runtime ready`,
   `provider ready`, `hosted ready`, `benchmark superior`,
   `benchmark validated`, `autonomous ready`, `MVP ready`, `release ready`,
   `broad user ready`) — 55 lines repo-wide — each read individually
   (table below).
2. Hits inside this lane's new or changed files (this packet directory,
   `tests/test_self_operator_closeout_guardrails.py`,
   `tests/test_self_operator_release_gate.py`,
   `alpha/self_operator/release_gate.py`, and the runbook section 5
   correction) — each read individually.
3. All remaining hits are unchanged from the #472-reviewed baseline: the
   same files, lines, and classifications recorded in
   `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-runbook-finalization-and-boundary-review/forbidden-claim-scan-results.md`
   apply unchanged (no pre-existing file in scan scope was modified by this
   lane except the runbook section 5 wording, whose hits are re-reviewed in
   tier 2).

## Tier 1: claim-type hits, individually classified

| Hits | Classification |
| --- | --- |
| `docs/.../release-closeout-and-final-guardrails/forbidden-claims.md` (10 lines: the blocked-claim list itself) | allowed_boundary_reference |
| `tests/test_self_operator_closeout_guardrails.py` (guardrail phrase constants the tests block) | allowed_boundary_reference |
| `docs/.../runbook-finalization-and-boundary-review/forbidden-claim-scan-results.md` (6 lines: prior scan record quoting patterns) | allowed_boundary_reference |
| `tests/test_self_operator_acceptance_interpretation.py` (2 lines: asserts rendered output excludes the phrases) | allowed_boundary_reference |
| `tests/fixtures/alpha_minimal_behavior_cases.json` (2 lines: deliberately unsafe input text in a rewrite-safely case) | irrelevant_false_positive |
| Prior self-operator packet blocked-claim / non-action negation lists (runbook section 16, `non-actions.md` files, claim-boundary registers, checklists, rubric) | allowed_boundary_reference |
| `docs/evals/batch-b/prompt-candidate-bank.md` (quoted unsafe operator request) | irrelevant_false_positive |
| `docs/evals/runs/alpha-solver-post-level-3-product-surface-threat-risk-model/abuse-cases.md`, `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md`, `docs/evals/runs/alpha-solver-post-level-3-quality-eval-artifact-schema/README.md` (overclaim-detection and non-claim template references) | allowed_boundary_reference |
| This packet's `forbidden-claim-scan-results.md` and `checks-run.md` (scan command and pattern documentation) | allowed_boundary_reference |

No tier-1 hit asserts readiness as a project status claim.

## Tier 2: this lane's new/changed-file hits

Every hit inside this packet, the guardrail test module, and the corrected
runbook section is one of:

- the blocked-claim list in `forbidden-claims.md` (allowed_boundary_reference);
- negated boundary enumerations in `evidence-boundary.md`,
  `non-actions.md`, and `boundary-status.md` (allowed_boundary_reference);
- the checker's own recorded non-action strings in
  `post-closeout-release-gate-report.json` / `.md`
  (allowed_boundary_reference);
- guardrail test constants that exist to block the phrases
  (allowed_boundary_reference);
- the runbook's pre-existing blocked-surface and blocked-claims sections,
  unchanged by this lane (allowed_boundary_reference);
- scan/check command documentation in this file and `checks-run.md`
  (allowed_boundary_reference).

## Action taken for forbidden_claim hits

None required: zero hits classified as `forbidden_claim`.

## Final scan decision

`pass` — classifications: allowed_boundary_reference and
irrelevant_false_positive only; forbidden_claim count is zero.
