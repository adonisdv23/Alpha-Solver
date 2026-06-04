# Measurement Readiness Checklist

Status: planning-only checklist for a future post-improvement measurement lane.

## 1. Evidence readiness

- [ ] PR #263 portable-contract artifacts are present.
- [ ] PR #262 offline contract test plan and fixtures are present.
- [ ] PR #261 implementation-readiness review and decision matrix are present.
- [ ] Batch B artifacts are present and preserved.
- [ ] A3-1 artifacts are present and preserved.
- [ ] Batch B score math recomputes from committed CSVs: Plain 405, Alpha 455, Alpha delta +50, Alpha wins 8, Plain wins 4, Ties 0.
- [ ] A3-1 score math recomputes from committed CSVs: Plain 237, Alpha 228, Alpha delta -9.
- [ ] Prior-pilot interpretation remains conservative: A3-1 favored plain in a limited four-comparison run; Batch B favored Alpha in a limited 12-comparison pilot; combined evidence suggests prompt-set-dependent behavior.

## 2. Surface readiness

- [ ] The selected measurement surface explicitly includes PR #263's changed portable contract.
- [ ] The Alpha condition describes how `alpha_solver_portable.py` is loaded as the behavior contract.
- [ ] `/v1/solve` is not used as post-improvement evidence unless it is proven to consume the portable contract.
- [ ] Provider/model/routing behavior is not changed to make this measurement possible.
- [ ] Offline contract tests are not described as output-quality or runtime API proof.

## 3. Prompt-packet readiness

- [ ] A separate frozen prompt packet exists before capture.
- [ ] Final prompt text is not drafted in this planning packet.
- [ ] A3-1 and Batch B prompts are used only as design references, not as sole proof.
- [ ] Complexity-gradient slots guide fresh prompt construction.
- [ ] Contamination controls are recorded before scorer-facing materials are prepared.

## 4. Capture readiness

- [ ] Operator approval is recorded before capture.
- [ ] Capture instructions state the exact portable-contract loading procedure for the Alpha condition.
- [ ] Capture instructions prohibit runtime/provider/model/routing changes during the run.
- [ ] Capture instructions preserve sanitized output text and required metadata without raw provider payloads.
- [ ] Capture does not start Batch C.

## 5. Scorer readiness

- [ ] Scorer-facing packet is blinded.
- [ ] Scorer-facing packet excludes surface identity, provider identity, model identity, runtime notes, assignment patterns, and operator-only unblinding material.
- [ ] The same 14 rubric dimensions are used unless changed in a separate approved PR.
- [ ] Scoring instructions prohibit validation, superiority, production-readiness, benchmark-success, exact-billing, broad-runtime-readiness, and provider-orchestration claims.

## 6. Artifact preservation readiness

- [ ] Frozen prompt packet, capture packet, source packet, scorer packet, score tables, defects, unblinding map, and run summary have named locations.
- [ ] Score tables preserve comparison-level totals and dimension scores.
- [ ] Defect notes preserve invented scaffolding, verbosity, claim-boundary, and stop-condition issues.
- [ ] Length/token fields are preserved if feasible without exact-billing claims.
- [ ] Sanitization notes confirm no raw provider payloads are introduced.

## 7. Unblinding readiness

- [ ] Unblinding map is operator-only until scoring is complete.
- [ ] Score table structure supports post-unblinding totals, wins, ties, and deltas.
- [ ] Lift, polish, and brevity cluster calculations are planned after approved unblinding.
- [ ] No scorer receives assignment patterns or source labels before scoring.

## 8. Non-claim readiness

- [ ] No MVP validation claim.
- [ ] No Alpha Solver superiority claim generally.
- [ ] No broad plain-provider inferiority claim.
- [ ] No answer-quality superiority claim generally.
- [ ] No production-readiness claim.
- [ ] No broad runtime-readiness claim.
- [ ] No benchmark-success claim.
- [ ] No exact-billing claim.
- [ ] No provider reasoning orchestration claim.

## 9. Stop conditions

Stop the future measurement lane if any of these occur:

- Measurement surface does not include PR #263 change.
- Final prompt packet is not frozen.
- Scorer packet is unblinded.
- Provider/capture environment is unavailable.
- Existing artifacts are missing.
- Raw provider payload handling is unclear.
- Capture would be run before operator approval.
- Runtime/provider/model/routing changes are needed.
- Batch C would be started.
