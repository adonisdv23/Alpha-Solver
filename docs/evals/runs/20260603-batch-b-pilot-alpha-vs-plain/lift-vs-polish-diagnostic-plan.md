# Lift-vs-Polish Diagnostic Plan

Status: diagnostic plan only

Lane: `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`

This artifact is a committed-evidence diagnostic plan. It does not run capture, rescore outputs, change runtime behavior, change provider behavior, change model configuration, change routing, update external planning ledgers, or start Batch C.

## Purpose

Diagnostic question: how much of Batch B's +50 Alpha advantage appears to be substantive lift versus polish, verbosity, formatting, or reviewer-facing structure?

The goal is to design a conservative follow-up review path that separates expert-interrogation lift from surface presentation effects without changing the official Batch B scores or making broad product claims.

## Evidence basis

This plan uses only committed repository evidence:

- Batch B score sheet: `blinded-score-sheet.csv`.
- Batch B blinding map: `blinding-map.csv`.
- Batch B score table: `score-table.csv`.
- Batch B defects and caveats: `defects.md`.
- Batch B run summary: `run-summary.md`.
- Batch B interpretation review: `interpretation-review.md`.
- Batch B post-interpretation decision: `post-interpretation-decision.md`.
- Lift decision rule: `docs/evals/LIFT_DECISION_RULE.md`.
- Response quality rubric: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`.

## Definitions

- **Lift cluster**: the expert-interrogation dimensions defined by the committed lift decision rule: `d04_assumptions`, `d05_hidden_constraints`, `d06_risk_failure`, and `d14_comparative_value`.
- **Polish cluster**: the presentation dimensions defined by the committed lift decision rule: `d03_structure`, `d10_next_actions`, and `d12_brevity`.
- **Brevity**: the `d12_brevity` rubric dimension, used here as the committed score signal for whether an output was appropriately concise for the task.
- **Substantive lift**: a diagnostic-only indication that Alpha's advantage is concentrated in lift-cluster or other evidence/claim/risk dimensions rather than only in structure, next actions, length, or formatting.
- **Polish-sensitive win**: an Alpha win that could plausibly be reduced or reversed if verbosity, headings, scaffolding, or reviewer-facing structure were compressed.
- **Diagnostic-only finding**: an interpretation used to choose future review questions; it does not alter official scores and is not validation evidence by itself.
- **Future capture**: any later collection of new Alpha/plain outputs, allowed only after explicit operator approval and a frozen run plan.
- **Future rescore**: any later blinded scoring pass, length-strip review, lift-only adjudication, or other scoring review, allowed only after explicit operator approval and with the official Batch B score left unchanged unless a separate approved artifact says otherwise.

## Current committed summary

- Batch B aggregate: Plain 405, Alpha 455, Alpha delta +50.
- Batch B wins: Alpha 8, Plain 4, ties 0.
- Lift cluster: Plain 111, Alpha 132, Alpha delta +21.
- Polish cluster: Plain 87, Alpha 86, Alpha delta -1.
- Brevity (`d12_brevity`): Plain 26, Alpha 16, Alpha delta -10.
- A3-1 counter-evidence remains important: Plain 237, Alpha 228, Alpha delta -9, and Plain won all four limited A3-1 comparisons.
- Interpretation: current evidence suggests Alpha's Batch B advantage was not merely polish, but brevity remains a serious weakness and diagnostic pressure is needed before over-reading the +50 result.
- Token, cost, and exact latency effects are not inferred because token and cost fields were not captured.
- No new capture is authorized by this plan.

## Per-comparison diagnostic matrix summary

The derived diagnostic matrix is `lift-vs-polish-diagnostic-matrix.csv`. It recomputes Alpha-minus-plain total, lift-cluster, polish-cluster, and brevity deltas from the committed Batch B CSVs after approved unblinding.

### Strongest substantive-lift candidates

- `cmp-B1-CAND-001`: Alpha +10 total, +3 lift, +1 polish, +1 brevity; strongest claim-boundary and evidence-needed release-wording candidate.
- `cmp-B1-CAND-020`: Alpha +20 total, +6 lift, +3 polish, -1 brevity; strong protocol checklist and preservation-boundary candidate.
- `cmp-B1-CAND-021`: Alpha +24 total, +10 lift, +2 polish, -2 brevity; strongest truthful-alternative and evidence-boundary candidate.
- `cmp-B1-CAND-009`: Alpha +5 total, +4 lift, -1 polish, -1 brevity; lift-led public-claim-control candidate.
- `cmp-B1-CAND-007`: Alpha +3 total, +1 lift, 0 polish, -2 brevity; substantive safety and claim-cleanup candidate, but high brevity risk.

### Possible polish-sensitive wins

- `cmp-B1-CAND-011`: Alpha +1 total, +1 lift, 0 polish, 0 brevity; narrow completeness win that should be tested under compression.
- `cmp-B1-CAND-013`: Alpha +3 total, +2 lift, -1 polish, -1 brevity; likely substantive constraint value, but over-extension could affect reviewer preference.
- `cmp-B1-CAND-022`: Alpha +3 total, +1 lift, 0 polish, 0 brevity; artifact-preservation explanation win with narrow margin.

### Wins that require diagnostic caution

- `cmp-B1-CAND-007`: high priority because the win was narrow and Alpha lost two brevity points.
- `cmp-B1-CAND-011`: high priority because the total margin was only +1 and defects noted excessive length.
- `cmp-B1-CAND-013`: high priority because defects noted optional system-design expansion beyond the prompt.
- `cmp-B1-CAND-022`: medium priority because the margin was narrow and assumptions about scoring emphasis were noted.

### Plain wins that expose brevity or format-fit risk

- `cmp-B1-CAND-005`: Plain -5 Alpha delta, with Alpha -2 polish and -2 brevity; strongest reviewer-comment format-fit warning.
- `cmp-B1-CAND-015`: Plain -8 Alpha delta, with Alpha -4 lift; strongest short-answer and non-invention warning.
- `cmp-B1-CAND-003`: Plain -3 Alpha delta; direct operator trust-rule fit beat Alpha's longer answer.
- `cmp-B1-CAND-017`: Plain -3 Alpha delta; clean safe rewrite beat Alpha's over-designed process framing.

### Priority for future length-strip or forced-concise review

High-priority comparisons for future length-strip or forced-concise review are `cmp-B1-CAND-005`, `cmp-B1-CAND-007`, `cmp-B1-CAND-011`, `cmp-B1-CAND-013`, `cmp-B1-CAND-015`, `cmp-B1-CAND-020`, and `cmp-B1-CAND-021`. Medium-priority comparisons are `cmp-B1-CAND-003`, `cmp-B1-CAND-009`, `cmp-B1-CAND-017`, and `cmp-B1-CAND-022`. `cmp-B1-CAND-001` remains high value for claim-boundary review, but its positive brevity delta makes it less central to brevity-only diagnosis.

## Diagnostic questions

- Does Alpha still win when verbosity and formatting are compressed?
- Which Batch B wins survive a length-strip review?
- Which wins are driven by claim-boundary, evidence uncertainty, hidden constraints, risk/failure, or comparative value?
- Which wins are narrow enough to require caution?
- Where does Alpha's brevity deficit erase or reduce its lift?
- Which prompt families predict Alpha gain versus Alpha loss?

## Proposed diagnostic experiments, future only

These experiments are designed but not executed by this plan.

### A. Length-strip rescore

- Compress Alpha winning outputs to a similar length as plain outputs.
- Strip nonessential headings and scaffolding.
- Preserve substantive claims and safety caveats.
- Blind re-score only after operator approval.
- Purpose: estimate whether Alpha wins survive reduced polish and length.

### B. Forced-concise Alpha variant

- Future run with Alpha instructed to answer first and keep optional detail minimal.
- No live run occurs in this PR.
- Purpose: test whether Alpha can preserve lift while improving `d12_brevity`.

### C. Prompt-family split

- Classify existing Batch B prompts by family.
- Identify families where Alpha won strongly, narrowly, or lost.
- Purpose: define candidate engagement criteria.

### D. Lift-only adjudication

- Recompute or review results using lift-cluster dimensions only.
- Do not change the official score.
- Purpose: separate official result from diagnostic lift signal.

### E. Gate simulation

- Create a retrospective decision rule for whether Alpha should engage expert behavior.
- Apply only on paper to A3-1 and Batch B prompts.
- Purpose: identify candidate conditions for a future selective-engagement planning lane.

### F. Complexity-gradient plan

- Design a future balanced prompt set from low to high headroom.
- No capture occurs in this PR.
- Purpose: test whether Alpha benefit increases with hidden constraints, claim-boundary risk, and artifact/protocol complexity.

## Acceptance criteria for a future diagnostic run

A future diagnostic run should not begin unless all of the following hold:

- Explicit operator approval before any new capture or rescore.
- Frozen packet before scoring.
- No route leakage.
- No unblinding before scoring.
- Raw-output safety boundaries are preserved.
- Token or length fields are recorded if feasible, without exact-billing claims.
- Diagnostics alone do not support MVP, superiority, production-readiness, broad runtime, benchmark, exact-billing, or provider-orchestration claims.

## How this informs future lanes

- `ALPHA-BREVITY-CONTROL-001`: identifies high-priority brevity-risk comparisons and prompt families where concise format-fit beat Alpha's expansion.
- `ALPHA-ANSWER-STRUCTURE-V2-001`: separates tasks where structured checklists helped from tasks where reviewer-facing structure became over-answering.
- `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`: preserves the strong claim-boundary signal while highlighting remaining invented-metric, causal-wording, and unsupported-detail caveats.
- `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`: provides paper-only candidate cues for when expert behavior may help or hurt, without implementing routing or provider orchestration.
- `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`: defines what later post-improvement measurement would need to test after approved brevity, structure, and claim-boundary planning work.

## Not authorized

This plan does not authorize:

- New capture.
- Live providers.
- Rescoring.
- Runtime change.
- Provider orchestration.
- Routing.
- Batch C.
- Production readiness.
- Public validation claim.

## Recommended next operator decision

Use this diagnostic plan to decide whether to run a future diagnostic review before or after targeted planning specs.

Recommended default: finish `ALPHA-BREVITY-CONTROL-001` and `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`, then decide whether to run the diagnostic before implementation.

## Non-claims

This diagnostic plan makes the following explicit non-claims:

- No MVP validation.
- No Alpha Solver superiority generally.
- No broad plain-provider inferiority.
- No answer-quality superiority generally.
- No production readiness.
- No broad runtime readiness.
- No benchmark success.
- No exact billing accuracy.
- No provider reasoning orchestration.
