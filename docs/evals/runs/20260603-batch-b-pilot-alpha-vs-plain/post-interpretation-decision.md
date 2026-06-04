# Post-Interpretation Decision

Status: decision artifact for operator review.

This decision artifact follows PR #251, which populated the official Batch B pilot scored artifacts, and PR #252, which added the Batch B interpretation review. It uses committed A3-1 and Batch B artifacts only. It does not rerun capture, rescore outputs, unblind new material, change dimension scores, change the scoring rubric, or change runtime behavior.

## Decision summary

Decision: proceed to targeted Alpha improvement planning and diagnostic planning.

This decision authorizes planning work only. It does not authorize:

- runtime implementation;
- provider, model, or routing changes;
- provider reasoning orchestration;
- production readiness work;
- public validation claims;
- Batch C implementation;
- new capture runs.

## Evidence basis

The decision uses the following committed repo artifacts:

### A3-1 evidence

- `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/run-summary.md`
- `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/score-table.csv`
- `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/defects.md`

### Batch B scored artifacts

- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/README.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/artifact-build-checks.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/source-packet.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blind-scorer-result.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinded-score-sheet.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinding-map.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/defects.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/run-summary.md`

### Batch B interpretation review

- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`

### Eval control docs and templates

- `docs/evals/LIFT_DECISION_RULE.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/BLIND_SCORING_PROCEDURE.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`
- `docs/evals/templates/comparison_score_table_template.csv`
- `docs/evals/batch-b/prompt-candidate-bank.md`
- `docs/evals/batch-b/execution-protocol.md`
- `docs/evals/batch-b/pilot-run-plan.md`
- `docs/evals/batch-b/post-capture-scoring-workflow.md`

## Decision rationale

A3-1 showed a limited plain-favoring result: Plain = 237, Alpha = 228, Alpha delta = -9, with plain winning all four limited comparisons.

Batch B showed a limited Alpha-favoring result: Plain = 405, Alpha = 455, Alpha delta = +50, with Alpha wins = 8, plain wins = 4, and ties = 0.

The combined evidence is prompt-set-dependent. A3-1 favored plain in a limited four-comparison run, while Batch B favored Alpha in a limited 12-comparison pilot. This supports targeted planning, not an immediate implementation jump or broad validation claim.

Batch B supports targeted planning because the lift cluster was positive while the polish cluster was not the driver: lift cluster Plain = 111, Alpha = 132, Alpha delta = +21; polish cluster Plain = 87, Alpha = 86, Alpha delta = -1. This indicates the next work should diagnose and preserve substantive lift rather than optimize for reviewer-facing polish or answer length.

Brevity remains the clearest negative signal. Batch B dimension aggregation recorded `d12_brevity` Plain = 26, Alpha = 16, Alpha delta = -10. Plain wins clustered around concise operator communication, format fit, short-answer fit, and avoiding over-designed process. Alpha wins were strongest around claim-boundary discipline, evidence hygiene, unsafe instruction cleanup, protocol/framing discipline, and artifact preservation.

Therefore, this decision authorizes planning lanes for brevity control, claim-boundary calibration, task aware answer structure, lift-versus-polish diagnosis, and selective expert engagement analysis. It does not authorize runtime implementation before a planning/spec PR, approved acceptance criteria, and an approved test or eval plan.

## Authorized next lanes

| Lane ID | Purpose | Evidence basis | Authorized output | Status | Explicit non-claims / limits |
| --- | --- | --- | --- | --- | --- |
| `ALPHA-BREVITY-CONTROL-001` | Reduce over-answering and improve short-answer-first behavior. | `d12_brevity` Alpha delta -10; plain wins on concise tasks. | Docs/spec proposal only, with acceptance criteria. | Ready | Not authorized: runtime change until operator approves implementation. No answer-quality superiority claim. |
| `ALPHA-ANSWER-STRUCTURE-V2-001` | Define task aware answer formats that preserve Alpha's evidence discipline while avoiding unnecessary process. | Plain wins on reviewer comments, short explanation, direct rewrite; Alpha wins on protocol, artifact, and claim tasks. | Docs/spec proposal only. | Refine | Not authorized: broad answer-quality claim or production readiness claim. |
| `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001` | Improve unsupported validation, causality, readiness, and superiority wording. | Alpha wins showed claim-boundary value; defects still flagged invented metrics and causal wording. | Docs/spec proposal or test plan. | Ready | Not authorized: MVP validation claim or Alpha Solver superiority generally. |
| `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001` | Plan a future engagement gate that decides when Alpha should apply expert/interrogation behavior. | A3-1 versus Batch B prompt-set-dependent behavior; plain wins on concise/format-fit tasks. | Planning memo only, no runtime implementation. | Verify | Not authorized: routing or live gate implementation yet; no provider reasoning orchestration claim. |
| `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001` | Design a diagnostic plan to separate substantive lift from polish/verbosity effects. | Lift cluster +21, polish cluster -1, brevity -10, and advisory review consensus aligned with committed evidence. | Diagnostic plan only. | Ready | Not authorized: new capture until operator approves. No benchmark success claim. |
| `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001` | Future re-measurement after approved improvements. | Re-measurement is required after approved changes land. | Future run plan only after improvements. | Blocked pending approved improvements | Not authorized: immediate capture, Batch C implementation, or public validation claim. |

## Not authorized lanes

| Held lane | Why it remains held |
| --- | --- |
| Provider reasoning orchestration | The evidence supports planning and diagnostics only; it does not justify provider-level orchestration work. |
| Tool routing | Prompt-set-dependent evidence does not authorize routing changes or tool routing implementation. |
| Persistent quota | The decision artifact has no evidence basis for quota persistence work and does not address runtime resource management. |
| Cost/latency optimization | Batch B token/cost fields were not captured, so exact cost or latency optimization is not evidence-backed here. |
| Production readiness | Neither A3-1 nor Batch B establishes production readiness or broad runtime readiness. |
| Public claims / marketing validation | The evidence is limited and prompt-set-dependent, so public validation, benchmark, superiority, and broad inferiority claims remain blocked. |
| Batch C runtime implementation | Batch C is not started by this decision and remains blocked until selected planning and approved improvements justify a future run plan. |
| New live capture | New capture remains blocked until an approved diagnostic or post-improvement run plan exists. |

## Decision gates before implementation

1. Operator approval of this decision artifact.
2. Planning/spec PR for the selected next lane.
3. Acceptance criteria approved by the operator.
4. Tests or eval plan defined before implementation.
5. No runtime implementation before spec approval.
6. No post-improvement run before approved improvements land.

## Recommended order

1. `ALPHA-BREVITY-CONTROL-001`
2. `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`
3. `ALPHA-ANSWER-STRUCTURE-V2-001`
4. `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`
5. `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`
6. Decide whether to implement minimal behavior changes.
7. `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001` only after approved improvements.

This order prioritizes the strongest negative signal first, then protects the strongest positive evidence area, then refines answer shape, diagnoses lift versus polish before additional measurement, and only then plans selective engagement. The sequence avoids building orchestration or launching new capture before the diagnostic objective and acceptance criteria are clear.

## Risks

- Over-reading Batch B as a broad validation result.
- Dismissing A3-1 rather than treating the combined evidence as prompt-set-dependent.
- Optimizing for verbosity or reviewer-facing structure instead of substantive lift.
- Building orchestration too early.
- Implementing runtime changes before spec approval.
- Launching new evals before clarifying the diagnostic objective.
- Turning prompt-set-dependent evidence into broad product claims.

## Non-claims

This decision makes the following explicit non-claims:

- No MVP validation.
- No Alpha Solver superiority generally.
- No broad plain-provider inferiority.
- No answer-quality superiority generally.
- No production readiness.
- No broad runtime readiness.
- No benchmark success.
- No exact billing accuracy.
- No provider reasoning orchestration.

## Operator next step

1. Review and merge this decision PR.
2. Update GS Backlog Master after merge.
3. Then start the first approved planning lane.
