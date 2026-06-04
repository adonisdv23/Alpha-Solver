# Results Import Review Checklist

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-REVIEW-GATE-001`

Use this checklist when reviewing the future `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-001` PR. The checklist is a gate for import integrity only. It does not ask the reviewer to score, rescore, validate, benchmark, or interpret the operator feedback.

## 1. Source evidence

- [ ] The PR identifies Adonis as the operator or explains the approved operator substitution.
- [ ] The PR includes actual operator-provided evidence for each imported task row.
- [ ] The evidence provenance is clear enough to distinguish operator-provided feedback from repo-authored templates.
- [ ] The source evidence is from the manual portable Alpha behavior-contract test, not `/v1/solve`, runtime APIs, live providers, Batch C, scoring, rescoring, capture, unblinding, raw outputs, operator-only maps, or Google Sheets.
- [ ] Google Sheets, if mentioned, is not treated as proof by itself.
- [ ] The PR does not require the reviewer to inspect private materials, secrets, raw provider payloads, full unredacted traces, or operator-only maps.
- [ ] The PR does not reconstruct missing evidence from memory, prior expectations, planning ledgers, or blank templates.

## 2. Result log integrity

- [ ] Every imported row maps to a task that was actually run by the operator.
- [ ] No task row is created for a task that was skipped, only planned, or not evidenced.
- [ ] Task IDs match the prepared task set (`LT-001` through `LT-010`) when those tasks were actually run.
- [ ] The task family is copied from the prepared task set or from operator evidence, not invented during import.
- [ ] The operator name, test date, test surface, portable-surface context, and provenance fields are present where the future import schema requires them.
- [ ] Missing fields remain blank or explicitly marked missing; they are not inferred.
- [ ] Ratings are limited to integers `0`, `1`, `2`, or `3`.
- [ ] Missing ratings are not averaged, backfilled, normalized, translated, or converted into scores.
- [ ] `keep_refine_reject` is imported only if actually provided by the operator.
- [ ] Notes are operator feedback only and do not become benchmark conclusions.

## 3. Feedback consistency

- [ ] Each imported rating is supported by corresponding operator evidence.
- [ ] Each response snippet is sufficient to explain the rating or defect without committing excessive output.
- [ ] Snippets avoid private data, secrets, raw provider payloads, full unredacted traces, and any data outside the allowed manual operator-test surface.
- [ ] Snippets are not edited in a way that changes meaning.
- [ ] The import does not turn qualitative feedback into validation, readiness, superiority, runtime, provider, production, or billing claims.
- [ ] If the operator feedback is incomplete, the import describes it as incomplete and does not declare a completed feedback set.
- [ ] If evidence is ambiguous, the PR asks for refinement instead of filling gaps.

## 4. Defect log integrity

- [ ] Defects are imported only when actually observed by the operator.
- [ ] No defect is created merely because the template contains a defect taxonomy item.
- [ ] Each defect has a task ID, severity, description, evidence snippet, and suggested refinement when supplied by the operator.
- [ ] The primary defect for a task is clear, or the PR marks it as unclear rather than choosing one without evidence.
- [ ] Defects do not include private data, secrets, raw provider payloads, full unredacted traces, raw outputs, or operator-only map content.
- [ ] Defects are treated as usability/refinement feedback, not proof of broad failure or broad success.

## 5. Stop-condition review

- [ ] The future import records whether a stop condition was reached for every task actually run.
- [ ] If a stop condition was reached, the stop-condition ID or concise summary is included.
- [ ] If stop-condition status is missing, the PR is blocked until the status is provided or the row is removed.
- [ ] Stop-condition evidence snippets are the smallest safe snippets needed to support the import.
- [ ] The PR does not continue importing downstream rows after an operator-recorded stop unless the operator evidence clearly says testing resumed safely.
- [ ] The PR does not convert a stop condition into readiness, validation, benchmark, runtime, or provider conclusions.

## 6. Preservation boundaries

- [ ] The PR is docs-only and limited to the approved future results-import scope.
- [ ] The PR does not modify `alpha_solver_portable.py`.
- [ ] The PR does not modify `/v1/solve`, runtime API files, provider adapters, model configuration, routing, or capture scripts.
- [ ] The PR does not modify scoring rubrics, scored artifacts, raw outputs, sanitized scorer-facing packets, or operator-only maps.
- [ ] The PR does not update Google Sheets integrations or treat spreadsheet status as proof.
- [ ] The PR does not modify Batch C materials or production-readiness docs.
- [ ] The PR does not unblind, score, rescore, call providers, start capture, start Batch C, or use `/v1/solve`.

## 7. Claim boundaries

- [ ] The import states that the material is operator feedback only.
- [ ] The import does not claim benchmark success, validation, MVP readiness, production readiness, runtime readiness, Alpha superiority, broad Alpha-vs-plain generalization, broad plain-provider weakness, exact billing accuracy, self-healing, adaptive learning, self-optimization, autonomous optimization, or provider orchestration.
- [ ] The import does not claim `/v1/solve`, provider, model-routing, runtime, Batch C, production, or billing behavior was tested.
- [ ] The import does not imply that operator feedback is statistically representative.
- [ ] The import identifies a narrow next lane, if any, without starting Batch C or runtime/provider work.
