# Complexity-Gradient Holdout Plan

Status: future evaluation planning only

Lane: `OUTPUT-DIFF-COMPLEXITY-GRADIENT-HOLDOUT-PLAN-001`

This packet is a planning artifact for a future evaluation. It does not create final holdout prompts, run capture, rescore outputs, change runtime behavior, change provider behavior, change model configuration, change routing, update external planning ledgers, or start Batch C.

## 1. Purpose

Planning question: how should a future holdout be designed to test whether Alpha's value increases with prompt headroom while preserving brevity and claim-boundary discipline?

The purpose is to define prompt-family blueprints, slot definitions, sampling rules, contamination controls, and evaluation design criteria. This packet deliberately avoids final scored prompt text so a later holdout can be frozen without contaminating the future evaluation.

## 2. Evidence basis

This plan is derived from committed repository evidence only:

- A3-1 artifacts: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`.
- Batch B artifacts from the official pilot: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/`.
- Batch B interpretation review: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`.
- Batch B post-interpretation decision: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/post-interpretation-decision.md`.
- Batch B next-lane decision artifact: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/decision-next-lanes.md`.
- Brevity-control planning spec: `.specs/ALPHA-BREVITY-CONTROL-001.md`.
- Lift-vs-polish diagnostic plan: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/lift-vs-polish-diagnostic-plan.md`.
- Selective expert engagement plan: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/selective-expert-engagement-plan.md`.
- Claim-boundary calibration packet: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/claim-boundary-calibration-plan.md` and its companion claim-boundary taxonomy and scenario-bank artifacts.
- Eval control docs: `docs/evals/LIFT_DECISION_RULE.md`, `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/BLIND_SCORING_PROCEDURE.md`, `docs/evals/ARTIFACT_PRESERVATION.md`, and `docs/evals/templates/comparison_score_table_template.csv`.

## 3. Current evidence summary

- A3-1 aggregate: Plain = 237, Alpha = 228, Alpha delta = -9. Plain won all four limited comparisons.
- Batch B aggregate: Plain = 405, Alpha = 455, Alpha delta = +50. Alpha wins = 8, Plain wins = 4, Ties = 0.
- Batch B lift cluster: Plain = 111, Alpha = 132, Alpha delta = +21.
- Batch B polish cluster: Plain = 87, Alpha = 86, Alpha delta = -1.
- Batch B brevity dimension `d12_brevity`: Plain = 26, Alpha = 16, Alpha delta = -10.
- Interpretation: the combined evidence suggests prompt-set-dependent Alpha behavior. A3-1 favored plain in a limited four-comparison run, while Batch B favored Alpha in a limited 12-comparison pilot.
- Prompt family, complexity, claim-boundary risk, artifact/protocol risk, requested brevity, and evidence hierarchy likely mediate whether Alpha helps or hurts.

These facts support future diagnostic planning only. They do not support MVP validation, general Alpha Solver superiority, broad plain-provider inferiority, answer-quality superiority generally, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration claims.

## 4. Why a complexity-gradient holdout is needed

A3-1 and Batch B sampled different prompt regions. A3-1 was a limited four-comparison run where plain won every comparison. Batch B was a limited 12-comparison pilot with more Alpha-favorable behavior in several higher-headroom prompt families, especially where claim-boundary, evidence, unsafe-instruction cleanup, protocol, and artifact-preservation concerns were present.

The next measurement problem is not another broadly described Alpha-versus-plain run. It is a controlled future holdout that can separate low-headroom, medium-headroom, and high-headroom prompts while avoiding overfit to Batch B. The future design must separate task complexity from verbosity, polish, and prompt-family bias. It also must test whether concise Alpha behavior can preserve substantive lift without losing the short-answer discipline that helped plain in some prompts.

## 5. Headroom definitions

- **Low headroom**: simple, direct, low ambiguity, concise output expected. A strong answer is short, answer-first, and unlikely to benefit from added protocol, caveats, or expert interrogation.
- **Medium headroom**: some constraints, moderate evidence caveat, moderate structure needed. A strong answer may need one or two compact caveats, an ordering choice, or a short rationale, but over-expansion remains a failure mode.
- **High headroom**: hidden constraints, safety risk, source hierarchy issue, artifact preservation, claim-boundary risk, protocol complexity, or high cost of overclaiming. A strong answer may need explicit evidence discipline, stop conditions, preservation rules, or constrained alternatives, while still avoiding unsupported breadth.

## 6. Prompt-family buckets

A future holdout should draw from these prompt-family buckets without reusing final Batch B prompt text:

1. direct operator decision;
2. reviewer comment;
3. short reviewer explanation;
4. claim-boundary release wording;
5. public marketing claim control;
6. repo-vs-sheet evidence hierarchy;
7. unsafe coding-agent instruction cleanup;
8. artifact preservation stop condition;
9. raw payload preservation explanation;
10. protocol checklist;
11. implementation prompt;
12. evidence synthesis / interpretation.

The companion slot matrix assigns each family to low, medium, and high headroom slots using descriptions only.

## 7. Slot design

Recommended future holdout shape: 36 slots total.

- 12 low-headroom slots.
- 12 medium-headroom slots.
- 12 high-headroom slots.
- Balanced across the 12 prompt families, with one low, one medium, and one high slot per family.
- At least 6 concise-output slots.
- At least 6 claim-boundary-risk slots.
- At least 6 artifact/protocol-risk slots.
- At least 6 source-hierarchy/evidence-risk slots.
- At least 6 safe-rewrite or unsafe-instruction cleanup slots.

The 36-slot design is large enough to compare headroom bands and prompt families while still being small enough for careful artifact preservation and blinded scoring. If the operator later needs a cheaper diagnostic, a frozen prompt-packet PR could downsample to a balanced 18-slot design, but the default planning recommendation is 36 slots because prompt-family mediation is the core question.

Slot descriptions must remain abstract. They should specify the evaluation target, risks, expected response mode, and contamination controls, not the exact user prompt or final wording.

## 8. Holdout contamination controls

- Do not commit final scored prompt text until the operator approves a frozen packet.
- Use slot descriptions, not final prompts, in this planning artifact.
- Avoid training, tuning, prompt-adjusting, or manual response-pattern optimization on the exact future holdout prompts.
- Freeze prompts before capture.
- Keep the scorer packet blinded.
- Do not unblind before scoring is complete and preservation checks are recorded.
- Preserve the scorer-facing packet separately from the operator-only map.
- Do not mix prompt writing and scoring in one task.
- Keep metadata that could bias scorers, such as prompt family and headroom level, out of the scorer-facing packet unless the operator explicitly approves a design where that metadata is necessary.

Additional controls are detailed in `holdout-contamination-controls.md`.

## 9. Future scoring design

Recommended scoring design for a later operator-approved holdout:

- Use the same 14 rubric dimensions unless the operator approves a separate rubric-change proposal.
- Report total score, preference, defects, and per-dimension deltas.
- Preserve lift cluster and polish cluster reporting from the committed lift decision rule.
- Report `d12_brevity` separately because it is the clearest current negative dimension for Alpha.
- Include token or length fields if feasible, but do not make exact-billing claims from approximate length data.
- Preserve preference and defect notes as first-class artifacts.
- Keep prompt-family and headroom metadata separate from scorer-facing materials until after scoring, or keep it in an operator-only map if it risks scorer bias.
- Include source-hierarchy, artifact/protocol, claim-boundary, and safety/credential risk metadata for post-scoring diagnostic analysis.

## 10. Diagnostic questions the holdout should answer

- Does Alpha still lose low-headroom prompts?
- Does Alpha win high-headroom prompts without relying on verbosity?
- Does forced-concise Alpha preserve lift?
- Which prompt families trigger the strongest Alpha advantage?
- Which families should stay concise/plain-like?
- Do answer-structure and claim-boundary planning improve results?
- Does selective expert engagement have a plausible future gate?

## 11. Relationship to active planning lanes

- `ALPHA-BREVITY-CONTROL-001`: this plan supplies low-headroom and concise-output slots to test whether brevity controls reduce over-answering without hiding necessary caveats.
- `ALPHA-ANSWER-STRUCTURE-V2-001`: this plan can inform answer-first, compact-caveat, and protocol-depth expectations, but it does not edit or create that spec.
- `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`: claim-boundary slots test whether calibrated wording avoids validation, superiority, production-readiness, and benchmark overclaims.
- `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`: the low/medium/high headroom bands provide candidate gating evidence for when expert engagement may be useful versus when plain-like concision may be better.
- `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`: the holdout design preserves lift-cluster, polish-cluster, and brevity reporting so future analysis can distinguish substantive lift from surface presentation.
- `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`: this plan should inform a later post-improvement run only after the operator decides whether to implement minimal behavior changes and freezes a separate prompt packet.

## 12. Not authorized

This plan authorizes none of the following:

- final prompts;
- capture;
- scoring;
- rescoring;
- runtime implementation;
- provider orchestration;
- routing;
- Batch C;
- production readiness;
- public validation claim.

## 13. Recommended next operator decision

Do not run this holdout yet. Finish the planning lanes first. Then decide whether to implement minimal behavior changes before a future holdout.

If the operator chooses to run diagnostics before implementation, create a separate frozen prompt-packet PR. That later PR should include the final prompts, scorer-facing packet, operator-only map, artifact-preservation checklist, and stop conditions, and it should be reviewed before any capture begins.

## 14. Non-claims

This packet makes no claim of:

- MVP validation;
- Alpha Solver superiority generally;
- broad plain-provider inferiority;
- answer-quality superiority generally;
- production readiness;
- broad runtime readiness;
- benchmark success;
- exact billing accuracy;
- provider reasoning orchestration.
