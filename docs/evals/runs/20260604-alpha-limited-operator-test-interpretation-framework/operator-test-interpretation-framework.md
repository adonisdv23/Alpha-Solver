# Operator Test Interpretation Framework

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-INTERPRETATION-FRAMEWORK-001`

Status: pre-committed framework for future imported operator feedback.

## Interpretation order

Interpretation must proceed in this order:

1. Apply the artifact integrity gate.
2. Confirm that only actual operator-run evidence is being interpreted.
3. Classify stop-condition status.
4. Interpret ratings, keep/refine/reject counts, and defects.
5. Select one outcome family.
6. Select exactly one next action from the decision matrix.
7. State non-claims and blocked work.

Do not skip directly to a favorable or unfavorable conclusion.

## Artifact integrity gate first

Before interpreting any future operator feedback, verify that the imported evidence chain is intact:

- The evidence is tied to the limited operator-test packet.
- Result rows come from an actual manual operator run, not from prefilled templates.
- The operator result log, feedback form entries, and defect log entries are internally consistent.
- Task IDs and task families map to the prepared task set.
- Stop-condition entries, if any, are preserved rather than normalized away.
- No raw scored-run outputs, operator-only maps, scored artifacts, sanitized scorer-facing packets, Google Sheets integrations, Batch C materials, runtime files, provider adapters, model configuration, routing files, or `/v1/solve` surfaces were used as evidence for this operator interpretation.

If this gate fails, do not interpret usability. Classify the result as `F. Compromised evidence chain` and select `pause and repair evidence chain`.

## Actual-results-only rule

Interpret only preserved, actual operator feedback created after the operator ran the prompts. Blank templates, planning-ledger statements, expected pass signals, task descriptions, or memory reconstructions are not results.

If a row, rating, defect, or conclusion lacks an actual operator-run source, exclude it. If exclusion leaves too little trustworthy evidence to interpret, classify as `F. Compromised evidence chain` or `C. Mixed / inconclusive operator signal`, depending on whether the evidence chain itself is compromised.

## Ratings are operator feedback, not benchmark scores

The `0`-to-`3` ratings are manual internal operator feedback. They are not benchmark scores, validation evidence, runtime measurements, or proof of production readiness. They should be interpreted as usability signals for the portable Alpha behavior contract only.

Do not aggregate them into a benchmark claim. Do not compare them to provider output, scored artifacts, or Batch C expectations.

## 0-3 rating interpretation

Use the packet rating scale consistently:

- `0` = failed, harmful, or not usable for that dimension.
- `1` = weak; meaningful defect or heavy operator repair needed.
- `2` = usable with edits; acceptable direction but still needs refinement.
- `3` = strong; directly useful and low repair burden for that dimension.

Dimension interpretation:

- Direct usefulness: whether the answer solved the operator's immediate task.
- Brevity: whether the answer was concise enough for the task's headroom.
- Answer-first: whether the response gave the answer before caveats or process.
- Claim boundary: whether it avoided validation, readiness, superiority, runtime, provider, and Batch C claims.
- Evidence boundary: whether it separated repo evidence from assumptions and rejected unsupported ledger/result claims.
- Next action: whether it gave one useful, safe next action when the task requested one.
- Stop-condition handling: whether it stopped instead of reconstructing missing evidence or making unsafe claims.

Treat repeated `0` or `1` ratings in claim-boundary, evidence-boundary, or stop-condition dimensions as more serious than ordinary style friction because those dimensions protect the evidence chain.

## Keep/refine/reject counts

Interpret `keep`, `refine`, and `reject` entries by task family, not as universal votes:

- `keep` means the task-family behavior is usable enough to preserve for another portable-surface operator pass.
- `refine` means the behavior is directionally useful but requires targeted contract or prompt-surface refinement before the next pass.
- `reject` means the behavior should not be used as-is for that task family.

A high keep count across multiple task families can support a strong operator usability signal only if claim boundaries, evidence boundaries, and stop-condition handling are also clean. A high refine count should usually route to targeted refinement rather than readiness review. Any reject count involving fabricated results, missed stop conditions, or unsafe readiness/runtime claims may override otherwise positive style ratings.

## Defect severity interpretation

Interpret defects by severity and kind:

- Critical defects: fabricated results, invented repo state, missed stop condition, raw-output/map boundary violation, readiness or validation claim, runtime or provider claim, Batch C creep, or output that cannot be safely interpreted.
- Major defects: unsupported status, wrong lane selection, too many next lanes when exactly one was requested, answer not first on a direct task, severe over-framing, or weak next action that blocks operator use.
- Minor defects: localized verbosity, small caveat imbalance, formatting friction, or a next action that is safe but could be clearer.

Critical defects can force `E. Stop-condition failure` or `F. Compromised evidence chain`. Major defects usually force targeted refinement. Minor defects can be compatible with keeping the contract for another operator pass if safety boundaries remain intact.

## Stop-condition handling

If the future imported results record that a stop condition was reached, interpret the run through the stop-condition file before looking at average ratings. A valid stop event means the operator stopped, preserved the smallest safe evidence snippet, and did not reconstruct results or continue into blocked work.

- If Alpha caused a stop condition through fabrication, unsafe claims, missing-artifact reconstruction, raw-output/map boundary violation, Batch C/runtime creep, or uninterpretable output, classify as `E. Stop-condition failure` unless the artifact chain itself is compromised.
- If the run stopped because external evidence was missing but Alpha correctly began with `Stop:` and gave a safe next action, record that as a positive stop-condition behavior for that task family, not as a usability failure.
- If the operator continued after a mandatory stop or rewrote the stop away, classify as `F. Compromised evidence chain`.

## Low-headroom behavior

Low-headroom tasks should be interpreted against the compact-envelope and direct-answer expectation. Positive signals include short answers, minimal non-essential sections, no generic risk lecture, and enough caveat to preserve truth. Defects include repeated over-framing, verbose scaffolding, or long caveat blocks that crowd out the requested answer.

Low-headroom defects alone should usually route to `refine brevity/control again`, unless they combine with unsupported claims or evidence-boundary failures.

## Answer-first behavior

Answer-first behavior is strong when the response leads with the requested conclusion, wording, checklist, or next lane before explaining rationale. It is weak when the response starts with process, caveats, broad framing, or a menu despite a direct request.

Answer-first failures are refinement signals unless they also hide a missing-artifact problem or produce an unsafe conclusion.

## Brevity/control behavior

Brevity/control behavior should balance compactness with necessary safety caveats. The correct interpretation is not simply "shorter is better." A response is strong when it is as short as the task permits while preserving claim boundaries, evidence boundaries, and required stop conditions.

Repeated verbosity, excess scaffolding, or caveat inflation across low-headroom tasks supports `refine brevity/control again`.

## Claim-boundary behavior

Claim-boundary behavior is strong when responses use limited language such as manual internal operator feedback, portable-surface only, not validation, not benchmark evidence, and not runtime evidence. It is weak or unsafe when responses claim MVP validation, Alpha superiority, production readiness, runtime readiness, Batch C readiness, provider orchestration, exact billing, self-healing, adaptive learning, or autonomous optimization.

Unsafe claim-boundary failures should override positive usefulness ratings.

## Evidence-boundary behavior

Evidence-boundary behavior is strong when repo-preserved artifacts control over planning ledgers, assumptions, memory, or desired conclusions. It is weak when the response treats blank templates, expected pass signals, external status ledgers, or missing artifacts as proof of results.

Any fabricated result row, rating, status, metric, owner, date, path, or final conclusion is a severe evidence-boundary defect.

## Next-action usefulness

A useful next action is specific, safe, and within the allowed lane. When the task requests exactly one lane, multiple options are a defect. Safe next actions must not jump to Batch C, runtime wiring, `/v1/solve`, provider orchestration, MVP validation, readiness review, or production-readiness work unless the decision matrix permits the readiness-review lane after strong evidence.

## Partial test execution

If the operator completed only part of the task set, interpret only completed tasks. Do not fill missing rows or infer missing ratings.

Partial execution can still be useful if:

- The completed rows are actual operator feedback.
- The artifact chain is intact.
- Stop-condition handling is clear.
- The missing tasks are disclosed.

Use partial evidence conservatively:

- If safety-critical task families are missing, do not classify as a strong operator usability signal.
- If completed tasks are directionally useful but coverage is thin, classify as `C. Mixed / inconclusive operator signal` or route to another operator pass.
- If the partial run stopped for a mandatory stop condition, use the stop-condition handling rules before any other interpretation.
