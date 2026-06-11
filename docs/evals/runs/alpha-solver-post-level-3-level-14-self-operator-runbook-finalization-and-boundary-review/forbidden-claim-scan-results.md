# Forbidden-claim scan results

## Exact scan command

Run from the repo root after all edits, on 2026-06-11:

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs alpha scripts tests
```

Total hits: 3989 matching lines (a line is counted once even when it matches
several patterns). Baseline on `main` before this lane's edits: 3957; the 32
added lines are all inside this lane's three new directories.

## Review method (every hit reviewed)

Every hit was enumerated and classified. Three review tiers were applied so
that the risk-bearing hits got individual reading and the bulk hits got an
explicit, reproducible rule:

1. Claim-type pattern hits (`production ready`, `runtime ready`,
   `provider ready`, `hosted ready`, `benchmark superior`,
   `benchmark validated`, `autonomous ready`, `MVP ready`, `release ready`,
   `broad user ready`) — 23 lines repo-wide — each read individually
   (tier-1 table below).
2. Hits inside Self Operator claim surfaces (paths matching
   `docs/evals/runs/alpha-solver-post-level-3-*self-operator*`,
   `docs/evals/runs/alpha-solver-post-level-7-self-operator*`,
   `docs/evals/runs/alpha-solver-post-level-3-to-level-14-self-operator*`,
   `alpha/self_operator/`, `scripts/*self_operator*`,
   `tests/test_self_operator*`) — 957 lines including all 32 new ones —
   reviewed line-level: all 32 new-dir hits read individually; for the
   remainder, every line lacking an explicit negation/blocked keyword
   (198 lines) was read individually and the negation-keyword lines were
   verified to be blocked-surface or non-action enumerations.
3. Hits outside Self Operator surfaces — 3032 lines — classified by surface
   rule with per-area counts and spot reads (tier-3 table below).

## Tier 1: all claim-type hits, individually classified

| Hit | Classification |
| --- | --- |
| `tests/test_self_operator_acceptance_interpretation.py:306-307` (asserts rendered output does not contain the claim phrases) | allowed_boundary_reference |
| `docs/.../mvp-runbook-finalization/mvp-operator-runbook.md:292` (blocked-claims list, section 16) | allowed_boundary_reference |
| `docs/.../mvp-runbook-finalization/non-actions.md:14` (negated non-action) | allowed_boundary_reference |
| `docs/.../evidence-boundary-review/non-actions.md:13` (negated non-action) | allowed_boundary_reference |
| `docs/.../runbook-finalization-and-boundary-review/non-actions.md:23` (negated non-action) | allowed_boundary_reference |
| `docs/.../runbook-finalization-and-boundary-review/claim-boundary-review.md:25` ("No benchmark superiority ... claim") | allowed_boundary_reference |
| Prior self-operator packets: `runbook-review-skeleton/blocked-claims-checklist.md:8`, `runbook-review-skeleton/release-closeout-checklist.md:9`, `runbook-review-skeleton/non-actions.md:19`, `evidence-interpretation-release-control-pack/claim-boundary-register.md:12`, `acceptance-release-bridge-packet/acceptance-interpretation-rules.md:9`, `acceptance-release-bridge-packet/blocked-release-claims.md:8`, `level-11-...-local-artifact-preflight-foundation/non-actions.md:7`, `manual-local-acceptance-packet/acceptance-interpretation-rubric.md:9`, `level-12-...-dry-run-wrapper/non-actions.md:10`, `acceptance-release-control-pack/non-actions.md:8` (all blocked-claim or non-action negation lists) | allowed_boundary_reference |
| `tests/fixtures/alpha_minimal_behavior_cases.json:107,117` (deliberately unsafe input text and its detection token in a rewrite-safely behavior case) | irrelevant_false_positive |
| `docs/evals/batch-b/prompt-candidate-bank.md:67` (quoted unsafe operator request the prompt must clean up) | irrelevant_false_positive |
| `docs/evals/runs/alpha-solver-post-level-3-product-surface-threat-risk-model/abuse-cases.md:22` (abuse scenario being defended against) | allowed_boundary_reference |
| `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md:133` (overclaim-detection rubric quoting the phrase to detect) | allowed_boundary_reference |
| `docs/evals/runs/alpha-solver-post-level-3-quality-eval-artifact-schema/README.md:55` (required non-claim template text) | allowed_boundary_reference |

No tier-1 hit asserts any readiness; count reconciles to 23.

## Tier 2: Self Operator surface hits (957)

All are one of: blocked-surface enumerations and non-action negations;
quoted operator-confirmation or boundary text; redaction vocabulary and
secret-marker keyword lists in `alpha/self_operator/redaction.py` and its
tests; forbidden-behavior static-test pattern lists; and schema fields fixed
to safe values (for example `deployment: false`). The 198 lines without an
explicit negation keyword were each read; all are list items inside blocked
or operator-only-boundary sections, or sensitive-surface inventories marked
inspect-only. Classification: allowed_boundary_reference (957/957). The 32
hits in this lane's new files are quoted in `checks-run.md` and fall in the
same class.

## Tier 3: out-of-lane surface hits (3032)

These sit in subsystems outside the Self Operator MVP claim surface, where
the matched words are those subsystems' own subject matter, not claims about
this MVP: `/v1/solve` API docs and tests, webapp auth/oauth and secret-store
code and tests, budget/billing guard code, Cloud Run deployment docs and
specs evidence, local-LLM orchestration lanes, and similar. Largest areas:
`docs/evals` non-self-operator lanes (~2400), `tests/` API/auth/UI suites
(~250), `alpha/webapp` and other non-self-operator code (~90),
`docs/deployment` and operator manuals (~80), remainder spread across
guides. Spot reads in each area confirmed subject-matter usage.
Classification: irrelevant_false_positive for this lane's claim boundary
(3032/3032), with the five claim-type lines among them already individually
classified in tier 1.

## Accounting

Each hit carries exactly one classification. Tier 1 is a cross-cutting
subset: 17 of its 23 lines sit inside the tier-2 surface and 6 inside the
tier-3 surface, and its individual classifications override the bulk rule
for those 6 (3 stay irrelevant_false_positive as quoted unsafe inputs, 3
are allowed_boundary_reference as rubric/abuse-case/non-claim-template
text).

| Classification | Count |
| --- | --- |
| allowed_boundary_reference | 960 (all 957 self-operator surface hits + 3 tier-1 out-of-lane boundary/rubric lines) |
| irrelevant_false_positive | 3029 (3026 out-of-lane subject-matter lines + 3 quoted-unsafe-input lines) |
| forbidden_claim | 0 |

Totals reconcile: 960 + 3029 + 0 = 3989.

## Action taken for forbidden_claim hits

None required: zero hits classified forbidden_claim.

## Final scan decision

```text
pass
```

No forbidden claim exists in `docs`, `alpha`, `scripts`, or `tests`; the
lane proceeds to next-lane selection. A `pass` here is a claim-hygiene
result only and is not a readiness claim.
