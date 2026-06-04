# Evidence Packaging Standard

Standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`

Status: docs-only packaging standard. This document defines import packaging requirements and does not import, score, interpret, or validate operator-test results.

## Scope

This standard applies only to manual operator-test evidence produced from `ALPHA-LIMITED-OPERATOR-TEST-001` after the operator actually runs the portable Alpha behavior-contract test. It governs how Adonis packages evidence for later import review.

This standard does not authorize:

- importing actual results;
- fabricating or backfilling missing results;
- executing prompts;
- inspecting raw provider payloads or operator-only maps;
- updating Sheets;
- starting Batch C;
- using `/v1/solve`;
- modifying runtime, provider, model, routing, SAFE-OUT, budget guard, determinism, observability, replay, or `SolverEnvelope` behavior;
- claiming validation, production readiness, benchmark success, provider behavior, runtime behavior, or Alpha superiority.

## Required bundle structure

A packaged evidence bundle should be a separate artifact created after a real manual run. It should contain only sanitized, reviewable evidence needed to support later import.

Recommended bundle sections:

1. **Bundle metadata**
   - Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-001`.
   - Packaging standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`.
   - Operator name or approved pseudonym.
   - Test date using `YYYY-MM-DD`.
   - Test surface: `portable Alpha behavior contract only`.
   - Package date using `YYYY-MM-DD`.
   - Packager name.
2. **Task evidence index**
   - One row per task that was actually run.
   - Use only task IDs from the approved operator-test task set.
   - Include task family, status, redaction status, and whether a stop condition was reached.
3. **Sanitized result-log fields**
   - Fields copied from the operator result-log template when actually observed.
   - Missing fields explicitly marked with the missing-field markers in this standard.
4. **Operator feedback entries**
   - One sanitized feedback entry per task that was actually run.
   - Preserve operator notes, uncertainty, and wording except where redaction is required.
5. **Defect entries, if any**
   - Sanitized defect entries using the approved defect-log taxonomy.
   - Use evidence snippets, not full transcripts.
6. **Redaction log**
   - What category of content was redacted, why, and whether meaning was preserved.
   - Do not include the redacted secret or private value.
7. **Import-readiness checklist**
   - Completed checklist showing whether the bundle is import-ready or blocked.

## Accepted evidence types

Accepted evidence types are limited to sanitized artifacts that support the manual operator feedback without exposing sensitive or unsupported material:

- task ID and task family from the approved task set;
- operator name or approved pseudonym;
- test date;
- test surface label confirming portable Alpha behavior contract only;
- portable-surface context in concise, non-sensitive form;
- stop-condition yes/no and a short stop-condition ID or summary;
- operator ratings from the feedback form or result-log template, when actually entered by the operator;
- keep/refine/reject decision, when actually entered by the operator;
- concise operator notes, with private details redacted;
- defect ID, severity, taxonomy label, description, likely cause, suggested refinement, and block decision, when actually observed;
- short response snippets that are necessary to support a note or defect;
- redaction-log entries describing redaction categories without revealing the redacted content;
- missing-field markers that honestly identify absent information.

## Disallowed evidence types

Do not package:

- raw provider payloads;
- API request or response bodies;
- full unredacted transcripts;
- secrets, API keys, tokens, cookies, credentials, private URLs, or environment values;
- private personal data that is not necessary for review;
- operator-only maps, blinding maps, unblinding maps, or raw-output maps;
- Google Sheets contents as proof;
- hidden scores, Alpha/plain comparisons, benchmark rows, rescoring, or scoring interpretations;
- unsupported reconstructed details;
- results for tasks that were not actually run;
- generated or inferred ratings where the operator left the field blank;
- claims that the test proves validation, readiness, runtime behavior, provider behavior, production behavior, billing behavior, self-healing, adaptive learning, autonomous optimization, Batch C readiness, public launch readiness, or superiority.

## Response snippets versus full transcripts

Use response snippets only when they are needed to support operator feedback, a defect, or a stop-condition note.

A response snippet should:

- be as short as possible while preserving the relevant evidence;
- include enough neighboring context to avoid misrepresenting the answer;
- omit private data and sensitive content;
- be labeled as a snippet, not a complete transcript;
- identify the associated task ID;
- preserve wording relevant to the observed behavior, such as an unsupported claim or over-framing pattern;
- avoid quoting an entire response when a shorter excerpt supports the review.

A full transcript is blocked unless an approved reviewer separately authorizes a sanitized transcript for a specific reason. Even then, redact private data, secrets, raw provider payloads, and unsupported map content first.

## Task ID citation rules

Every evidence item must cite a task ID.

Use this format:

- `task_id: <approved-task-id>` for result rows, feedback entries, snippets, and defect entries.
- `related_task_ids: [<approved-task-id>, <approved-task-id>]` only when a note spans multiple actually run tasks.
- `task_id: UNKNOWN` is blocked unless the bundle includes an explicit remediation note explaining why the evidence cannot be imported until the task ID is recovered from approved operator notes.

Do not invent task IDs, normalize task IDs from memory, or infer task IDs from response content alone. If the task ID cannot be verified from the approved operator packet or operator notes, mark the bundle blocked.

## Preserving operator notes

Operator notes are evidence. Preserve the operator's meaning and uncertainty.

Packaging may:

- redact private data;
- replace names, identifiers, or sensitive facts with consistent placeholders;
- trim unrelated prose;
- normalize formatting into the result-log or feedback template;
- add a bracketed packaging note such as `[redacted private client name]`.

Packaging must not:

- improve the rating;
- downgrade the rating;
- rewrite a weak note into a stronger claim;
- convert uncertainty into certainty;
- add a rationale the operator did not provide;
- turn feedback into validation;
- summarize away a stop condition;
- delete defect evidence because it is inconvenient.

If a note is ambiguous, preserve the ambiguity and add `packaging_note: ambiguous; do not interpret during import`.

## Missing-field markers

Never fabricate missing fields. Use explicit markers:

- `NOT_PROVIDED` — the operator left the field blank or it is absent from the approved notes.
- `NOT_RUN` — the task was not run.
- `NOT_APPLICABLE` — the field does not apply to the observed task or defect.
- `REDACTED_PRIVATE` — private personal or organizational data was removed.
- `REDACTED_SECRET` — a secret, token, credential, cookie, key, or environment value was removed.
- `REDACTED_RAW_PAYLOAD` — raw provider/API payload content was removed.
- `BLOCKED_UNVERIFIED_TASK_ID` — the task ID cannot be verified.
- `BLOCKED_UNSUPPORTED_CLAIM` — the package contains a claim that must be removed or reframed before import.

Do not use numeric defaults such as `0`, `3`, or averages as placeholders for blank ratings.

## Avoiding fake precision

Manual operator feedback is not a benchmark score and not validation. Avoid fake precision by following these rules:

- Report only the integer ratings the operator actually recorded.
- Do not compute averages, percentages, deltas, confidence intervals, ranks, or pass rates.
- Do not compare Alpha against plain, prior batches, or external systems in this bundle.
- Do not infer statistical significance from a limited manual run.
- Do not use exact-looking language such as `100% ready`, `validated`, `passed`, or `superior`.
- Use qualitative framing: `operator feedback`, `observed by operator`, `reported in manual notes`, or `blocked for import`.

## Claim boundaries

Allowed framing:

- `Limited operator-test evidence packaged for import review.`
- `The bundle contains sanitized operator feedback only.`
- `This does not prove production readiness.`
- `This does not prove Alpha superiority.`
- `This does not prove /v1/solve behavior.`
- `This does not prove provider or model-routing behavior.`

Forbidden framing:

- `MVP validated.`
- `Alpha is superior.`
- `Production-ready.`
- `Runtime-ready.`
- `Benchmark passed.`
- `Provider orchestration works.`
- `Exact billing proven.`
- `Self-healing.`
- `Adaptive learning.`
- `Autonomous optimization.`
- `Batch C ready.`
- `Public launch ready.`

If a bundle includes forbidden framing, mark it blocked until the claim is removed or rewritten as limited operator feedback.

## Import-ready bundle definition

A result bundle is import-ready only when all of the following are true:

- every evidence item is tied to an approved, actually run task ID;
- each included rating or note is copied from an actual operator entry;
- missing fields use approved missing-field markers;
- snippets are short, sanitized, and necessary for review;
- full unredacted transcripts are absent;
- raw provider payloads are absent;
- secrets and private details are absent or redacted;
- operator-only maps and raw-output maps are absent;
- no hidden scores, rescoring, Alpha/plain comparisons, or benchmark conclusions are included;
- no unsupported readiness, validation, runtime, provider, Batch C, public launch, or superiority claims are included;
- the redaction log is complete enough for import review;
- the import-readiness checklist is completed and indicates no blocked condition.

## Blocked bundle definition

A result bundle is blocked when any of the following are true:

- it includes actual results for a task that was not run;
- it fabricates, infers, or defaults missing ratings or notes;
- it lacks verifiable task IDs;
- it exposes private data, secrets, raw provider payloads, full unredacted transcripts, or operator-only maps;
- it uses Google Sheets content as proof;
- it includes unsupported validation, readiness, benchmark, runtime, provider, billing, Batch C, public launch, or superiority claims;
- it interprets results, scores outcomes, compares systems, or imports rows;
- it reconstructs missing artifacts from memory or inference;
- it starts or references Batch C execution as an outcome of packaging;
- it changes protected runtime/provider/model/routing surfaces.

A blocked bundle may be remediated only by removing unsafe content, restoring verified task IDs from approved operator notes, replacing fabricated fields with missing-field markers, and completing the checklist again.
