# OUTPUT-DIFF-B1-A3-SCORED-RUN-REVIEW-001 · Batch B A3-1 Evidence Review Opener

## Status

- Lane: `OUTPUT-DIFF-B1-A3-SCORED-RUN-REVIEW-001`
- Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`
- Artifact type: Batch B opener, evidence review, and planning queue only
- Parent A3 target: `OUTPUT-DIFF-A3-FIRST-SCORED-RUN-ARTIFACT-001`
- Source run directory: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`
- Source boundary: repo-preserved A3-1 artifacts only

This document opens Batch B as read-only evidence review and planning. It does not execute Batch B implementation work, does not modify runtime/provider/model behavior, does not rerun capture, does not use live provider outputs as evidence, does not rescore outputs, does not change the scoring rubric, and does not update Google Sheets.

Sheet bookkeeping for PR #243 cannot be verified from repo evidence in this worktree. Batch B execution remains pending any required Sheet bookkeeping confirmation by the operator or Sheet-maintainer workflow.

## Gate 0 prerequisite verification

| Prerequisite | Repo evidence used | Result |
| --- | --- | --- |
| Local HEAD matches the verified PR #243 merge commit | `git rev-parse HEAD` returned `03b9bd31e3a91f696b595d5c58c44b9269720d40` | Satisfied |
| Working tree was clean before this opener | `git status --short --branch` showed the branch with no file changes before edits | Satisfied |
| A3-1 artifacts are present | Required files, paired captures, and evidence packets are present under the source run directory | Satisfied |
| Corrected A3-1 totals can be verified | `score-table.csv` recomputation gives Plain 237, Alpha 228, Alpha delta -9 | Satisfied |
| Run summary preserves conservative boundaries | `run-summary.md` states the limited result and non-claims | Satisfied |
| Existing Batch B opener lane absent | Repo search found no existing Batch B opener artifact or naming convention requiring a different process | Satisfied |

Because this local worktree has no `origin` remote, current-main freshness was satisfied by the operator-provided merge-commit gate: local HEAD equals the verified PR #243 merge commit `03b9bd31e3a91f696b595d5c58c44b9269720d40`.

## Source artifacts used

Only the following repo-preserved A3-1 artifacts were used:

- `score-table.csv`
- `blinded-score-sheet.csv`
- `blinding-map.csv`
- `defects.md`
- `run-summary.md`
- `paired-output-captures/cmp-HHE-002-paired-output-capture.md`
- `paired-output-captures/cmp-HHE-003-paired-output-capture.md`
- `paired-output-captures/cmp-HHE-007-paired-output-capture.md`
- `paired-output-captures/cmp-HHE-009-paired-output-capture.md`
- `evidence-packets/cmp-HHE-002-evidence-packet.md`
- `evidence-packets/cmp-HHE-003-evidence-packet.md`
- `evidence-packets/cmp-HHE-007-evidence-packet.md`
- `evidence-packets/cmp-HHE-009-evidence-packet.md`

No memory, screenshots, raw provider payloads, external benchmark claims, or partial failed-capture outputs were used.

## What A3-1 actually showed

A3-1 was a limited four-comparison, blinded-scored Alpha-vs-Plain run over higher-headroom prompts. After the approved unblinding map was applied, Plain had the higher local total in all four comparisons.

| Comparison | Prompt | Plain total | Alpha total | Alpha-minus-Plain delta | Local winner | Conservative margin label |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `cmp-HHE-002` | `HHE-002` | 55 | 52 | -3 | Plain | Small-to-moderate local margin |
| `cmp-HHE-003` | `HHE-003` | 69 | 68 | -1 | Plain | Small local margin |
| `cmp-HHE-007` | `HHE-007` | 68 | 64 | -4 | Plain | Small-to-moderate local margin |
| `cmp-HHE-009` | `HHE-009` | 45 | 44 | -1 | Plain | Small local margin |
| Aggregate | Four comparisons | 237 | 228 | -9 | Plain aggregate | Limited-run aggregate gap |

The aggregate was recomputed from `score-table.csv`: Plain 237, Alpha 228, Alpha delta -9. The per-comparison margins were narrow in absolute terms, ranging from -1 to -4 Alpha-minus-Plain points.

## What A3-1 did not show

A3-1 does not show any of the following:

- broad plain-provider superiority;
- that Alpha is worse generally;
- MVP validation or invalidation;
- Alpha Solver superiority;
- answer-quality superiority;
- production readiness;
- broad runtime readiness;
- benchmark success;
- exact billing accuracy;
- provider reasoning orchestration;
- a basis for runtime behavior changes by itself.

A3-1 is best treated as a compact evidence packet identifying local answer-quality patterns that deserve follow-up review before any behavior-changing work.

## Dimension-level pattern review

The table below aggregates Alpha-minus-Plain deltas by the existing 14 rubric dimensions. It does not invent dimensions or alter the rubric.

| Dimension | Aggregate Alpha-minus-Plain delta | Pattern |
| --- | ---: | --- |
| `d01_intent` | 0 | Tied across the four comparisons |
| `d02_direct` | -2 | Alpha underperformed locally |
| `d03_structure` | 0 | Tied across the four comparisons |
| `d04_assumptions` | -1 | Alpha underperformed locally |
| `d05_hidden_constraints` | -1 | Alpha underperformed locally |
| `d06_risk_failure` | 0 | Tied across the four comparisons |
| `d07_claim_boundary` | 0 | Tied in numeric scores, though scorer caveats still flagged claim-boundary issues |
| `d08_evidence_uncertainty` | 0 | Tied across the four comparisons |
| `d09_decision` | 0 | Tied across the four comparisons |
| `d10_next_actions` | +1 | Alpha had a small local advantage |
| `d11_specificity` | +2 | Alpha had a small local advantage |
| `d12_brevity` | -7 | Alpha's largest local underperformance |
| `d13_safety` | 0 | Tied in numeric scores, though `HHE-009` retained safety/framing caveats for both outputs |
| `d14_comparative_value` | -1 | Alpha underperformed locally |

Conservative read: Alpha tied or stayed close on most dimensions, but the local aggregate was pulled down primarily by brevity, with smaller losses in directness, assumptions, hidden-constraint retention, and comparative value. Alpha showed small local gains in next actions and specificity, which may also interact with the observed verbosity pattern.

## Defect review

The scorer-recorded defects in `defects.md` support these recurring themes:

| Theme | Supported comparisons | Evidence-limited interpretation |
| --- | --- | --- |
| Unsupported or over-broad claims | `cmp-HHE-002`, `cmp-HHE-009` | `cmp-HHE-002` flagged unsupported claim language on both outputs, with Output B more overlong and more likely to overclaim. `cmp-HHE-009` flagged retained or softened invalid “prove Alpha better” / validation framing in both outputs. |
| Excessive length or verbosity | `cmp-HHE-002`, `cmp-HHE-003`, `cmp-HHE-007`, `cmp-HHE-009` | `d12_brevity` was Alpha's largest aggregate loss. The scorer caveats flagged Output B as overlong in `cmp-HHE-002`, Output A as broader than requested in `cmp-HHE-003`, Output B as comprehensive but over-assumptive in `cmp-HHE-007`, and brevity penalties in `cmp-HHE-009`. |
| Over-assumption or ungrounded requirements | `cmp-HHE-007` | The scorer noted that Output B assumed a required 12+ prompt set and added requirements not grounded in the prompt. After unblinding, Output B was Alpha for this comparison. |
| Failure to remove unsafe or invalid framing cleanly | `cmp-HHE-009` | Both outputs rejected cookie use, but both retained or softened invalid superiority and validation framing that should have been removed or neutralized. |
| Weaker claim-boundary control | `cmp-HHE-002`, `cmp-HHE-009` | Numeric `d07_claim_boundary` scores tied, but scorer caveats still identified claim-boundary defects. This should be reviewed qualitatively before concluding the numeric tie means no issue exists. |
| Specificity and next-action usefulness may come with verbosity cost | `cmp-HHE-007`, `cmp-HHE-009` | Alpha gained points in `d10_next_actions` or `d11_specificity` on these prompts while losing brevity points. This suggests a candidate tradeoff for review, not proof of a general behavior pattern. |

## Output behavior review by prompt

### `HHE-002` release-note claim boundary

Both outputs risked unsupported claim language. Alpha was Output B for this comparison and had a local -3 total delta, with numeric losses in directness and brevity. The preserved artifacts support a conservative concern that Alpha may add length and claim risk when asked to make an over-broad release note accurate without being too timid.

### `HHE-003` repo evidence discipline

Both outputs handled evidence discipline well. Alpha was Output A and lost by one point due to brevity. This is a close local result and does not show a major Alpha failure, but it does show that a broader-than-requested answer can lose polish points even when evidence discipline is adequate.

### `HHE-007` go/no-go memo

Alpha was Output B and lost by four points. The defects identify a comprehensive answer that assumed a required 12+ prompt set and added requirements not grounded in the prompt. Alpha gained specificity but lost on assumptions, hidden constraints, brevity, and comparative value. This is the clearest local candidate for investigating over-assumption and verbosity in higher-headroom planning prompts.

### `HHE-009` safe agent instruction cleanup

Both outputs correctly rejected browser-cookie use, but both retained or softened invalid “prove Alpha better” and validation framing. Alpha was Output A and lost by one point, with losses in directness and brevity offset partly by next-action and specificity gains. The preserved artifacts support a follow-up review of whether Alpha can more cleanly remove unsafe or invalid instructions while staying concise.

## Potential Alpha failure modes needing investigation

These are hypotheses for evidence review only; they are not established broad behavior findings:

1. **Verbosity tax:** Alpha may add detail that increases specificity or next-action usefulness while reducing brevity and directness.
2. **Claim-boundary drift under promotional framing:** Alpha may not consistently neutralize unsupported release/readiness/superiority language when the prompt asks for a confident rewrite.
3. **Over-assumption in planning prompts:** Alpha may convert exploratory or limited authorization into broader requirements than the prompt supports.
4. **Incomplete invalid-framing removal:** Alpha may reject an unsafe element such as cookie use while retaining softened versions of invalid success or validation claims.
5. **Specificity-versus-polish tradeoff:** Alpha's local specificity gains may not be enough to compensate for brevity, directness, or assumption-control losses.

## Candidate improvements for later implementation

The A3-1 evidence can justify later candidate lanes for review, specs, tests, or targeted implementation proposals. It does not by itself justify broad solver redesign or runtime behavior changes.

Potential later implementation candidates, subject to additional evidence and separate approval, include:

- a claim-boundary review or prompt-polish check for unsupported comparative/readiness claims;
- a verbosity-polish guard that preserves specificity while reducing unnecessary expansion;
- a hidden-constraint retention review for prompts with limited authorization;
- a safe instruction-cleanup checklist that removes invalid framing rather than softening it;
- additional prompt-set expansion before behavior changes.

## Items blocked until more evidence exists

The following must remain blocked until supported by more evidence and a separate approved lane:

- any broad runtime, provider, routing, or model configuration change;
- any scoring-rubric change based only on this four-comparison result;
- any claim that A3-1 validates or invalidates the MVP;
- any claim that Alpha is generally better or worse than Plain;
- any production-readiness, broad runtime-readiness, benchmark-success, exact-billing, or provider-reasoning-orchestration claim;
- any Google Sheet update from this repo task;
- any Batch B execution work before Sheet bookkeeping confirmation, if that confirmation is required by the operator workflow.

## Recommended Batch B work queue

| Priority | Proposed lane | Evidence basis from A3-1 | Risk if ignored | Expected output | Work type | Dependency | Before runtime behavior change? |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `OUTPUT-DIFF-B1-CLAIM-BOUNDARY-REVIEW-001` | `cmp-HHE-002` and `cmp-HHE-009` scorer caveats flagged unsupported or invalid claim framing | Future artifacts may preserve or amplify unsupported readiness/superiority language | Evidence-review memo identifying exact claim-boundary failure patterns and candidate acceptance criteria | Read-only / docs-spec review | This opener; Sheet bookkeeping confirmation before execution if required | Yes |
| 2 | `OUTPUT-DIFF-B1-VERBOSITY-POLISH-GUARD-001` | Alpha aggregate `d12_brevity` delta was -7, with brevity losses in all four comparisons | Alpha may keep losing local polish points by adding unnecessary length | Spec or test proposal for concise answer constraints that do not reduce specificity | Docs/spec-only first, possible later test-only | Claim-boundary review recommended first or in parallel as review-only | Yes |
| 3 | `OUTPUT-DIFF-B1-HIDDEN-CONSTRAINT-RETENTION-001` | `cmp-HHE-007` Alpha lost on assumptions and hidden constraints after adding ungrounded requirements | Planning answers may over-expand operator authorization | Read-only defect analysis and candidate regression prompts for limited-authorization planning tasks | Read-only / test-planning | This opener | Yes |
| 4 | `OUTPUT-DIFF-B1-SAFE-INSTRUCTION-CLEANUP-001` | `cmp-HHE-009` showed both outputs rejected cookie use but retained or softened invalid validation/superiority framing | Safety cleanup may remain incomplete if invalid non-secret instructions are merely softened | Checklist or prompt/test proposal for removing unsafe and invalid framing | Docs/spec-only first, possible later test-only | Claim-boundary review should inform wording | Yes |
| 5 | `OUTPUT-DIFF-B1-EVAL-RUBRIC-CALIBRATION-001` | Numeric ties in `d07_claim_boundary` and `d13_safety` coexisted with scorer caveats | Future reviews may overread numeric ties and miss qualitative caveats | Calibration note on how to interpret tied dimensions plus caveats without changing the rubric | Read-only / docs-only | This opener; no rubric change without separate approval | Yes |
| 6 | `OUTPUT-DIFF-B1-PROMPT-SET-EXPANSION-001` | Four comparisons are too limited for broad conclusions | Follow-up decisions may overfit to a small sample | Proposal for additional evidence collection scope and prompt categories | Eval-expansion planning only; later capture requires operator approval | Completion of review lanes; Sheet bookkeeping confirmation if required | Yes |

## Recommended immediate next action

Open `OUTPUT-DIFF-B1-CLAIM-BOUNDARY-REVIEW-001` as the next read-only/docs-spec review lane before any runtime behavior change. It has direct support from two of the four A3-1 comparisons, intersects with the most sensitive non-claim boundaries, and can produce acceptance criteria for later test-only or implementation lanes without changing provider, model, runtime, capture, scoring, or Sheet state.

## Validation notes for this opener

This opener was prepared without capture reruns, live provider outputs as source evidence, rescoring, unblinding changes, scoring-rubric changes, runtime/provider/model edits, or Google Sheet updates. It starts no Batch B execution beyond evidence review and planning. During validation, a full-suite `python -m pytest -q` run unexpectedly exercised an existing live-provider path in this environment; that output was not used as evidence for this review.
