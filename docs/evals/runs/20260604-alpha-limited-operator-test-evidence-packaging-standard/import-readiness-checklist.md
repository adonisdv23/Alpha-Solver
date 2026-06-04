# Import Readiness Checklist

Standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`

Status: checklist template only. Do not complete this checklist with actual results until a manual operator-test bundle exists.

## Bundle identity

- [ ] Bundle cites lane ID `ALPHA-LIMITED-OPERATOR-TEST-001`.
- [ ] Bundle cites packaging standard ID `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`.
- [ ] Bundle identifies packager and package date.
- [ ] Bundle identifies operator name or approved pseudonym.
- [ ] Bundle identifies test date using `YYYY-MM-DD`.
- [ ] Bundle identifies test surface as `portable Alpha behavior contract only`.

## Task evidence

- [ ] Every evidence item cites an approved task ID.
- [ ] No task ID was invented, inferred, normalized from memory, or reconstructed from response content alone.
- [ ] Every included task was actually run.
- [ ] Tasks not run are either excluded or marked `NOT_RUN` without ratings or fabricated notes.
- [ ] Multi-task notes use `related_task_ids` and include only actually run task IDs.

## Result fields and operator notes

- [ ] Ratings are copied only from actual operator entries.
- [ ] Blank ratings are marked `NOT_PROVIDED` and not defaulted.
- [ ] `NOT_APPLICABLE` is used only where the field genuinely does not apply.
- [ ] Operator notes preserve meaning, uncertainty, and defect observations.
- [ ] Packaging notes are clearly labeled and do not add interpretation.
- [ ] Keep/refine/reject values are copied only when actually entered by the operator.
- [ ] Defects use the approved defect taxonomy when defects were observed.

## Snippets and transcripts

- [ ] Evidence uses short sanitized response snippets only when needed.
- [ ] Snippets are labeled `sanitized_response_snippet`.
- [ ] Snippets include enough context to support the operator note without misrepresenting the answer.
- [ ] Full unredacted transcripts are absent.
- [ ] Raw provider payloads are absent.
- [ ] API request or response bodies are absent.
- [ ] Google Sheets contents are not used as proof.

## Redaction and privacy

- [ ] Secrets, tokens, keys, credentials, cookies, and environment values are absent or marked `[REDACTED_SECRET]` or `[REDACTED_ENV_VALUE]`.
- [ ] Private people, organizations, URLs, account IDs, emails, phone numbers, and confidential business details are absent or redacted with approved placeholders.
- [ ] Operator-only maps, blinding maps, unblinding maps, and raw-output maps are absent.
- [ ] Redaction placeholders do not contain fake realistic replacement values.
- [ ] Redaction log lists redaction marker, reason, and whether meaning was preserved.
- [ ] Redaction log does not reveal the original redacted values.
- [ ] Sensitive details are absent from filenames, headings, metadata, comments, and screenshots.

## Claim boundaries

- [ ] Bundle frames findings as limited operator feedback only.
- [ ] Bundle does not claim validation, readiness, benchmark success, superiority, or production suitability.
- [ ] Bundle does not claim `/v1/solve`, runtime API, provider, model-routing, billing, self-healing, adaptive-learning, autonomous-optimization, provider-orchestration, Batch C, or public-launch behavior.
- [ ] Bundle does not include averages, percentages, deltas, confidence intervals, rankings, pass rates, or statistical conclusions.
- [ ] Any forbidden wording from the claim-boundaries packet has been removed or rewritten as limited operator feedback.

## Protected-surface confirmation

- [ ] Packaging did not execute prompts or tests.
- [ ] Packaging did not import rows or update Sheets.
- [ ] Packaging did not start Batch C.
- [ ] Packaging did not call `/v1/solve`.
- [ ] Packaging did not inspect raw outputs or operator maps.
- [ ] Packaging did not modify runtime/provider/model/routing or other protected implementation surfaces.

## Import decision

Choose exactly one:

- [ ] `IMPORT_READY` — all checklist items above are satisfied, no blocked condition remains, and the bundle contains only sanitized operator feedback evidence.
- [ ] `BLOCKED` — one or more checklist items failed, missing fields are unresolved, unsafe content remains, or unsupported claims remain.

If blocked, record the reason without exposing private data:

```yaml
bundle_status: BLOCKED
blocked_reason: <short reason using approved markers where needed>
required_remediation: <specific remediation before import review>
```
