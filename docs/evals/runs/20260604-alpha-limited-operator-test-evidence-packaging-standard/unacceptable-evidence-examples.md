# Unacceptable Evidence Examples

Standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`

Status: examples are synthetic anti-patterns only. They are not actual operator-test results.

## Unacceptable: full unredacted transcript

```text
Task: <task id>
Full response: <entire unredacted answer pasted here with private names, private links, and internal context>
```

Why blocked:

- exposes more text than needed for import review;
- may contain private data or unsupported claims;
- violates the snippet-first requirement.

Remediation:

- replace with the shortest sanitized snippet needed to support the operator note or defect;
- add redaction-log entries for removed private or sensitive content.

## Unacceptable: raw provider payload

```json
{
  "request": "<raw provider request>",
  "response": "<raw provider response>",
  "headers": {"authorization": "<secret>"}
}
```

Why blocked:

- raw provider/API payloads are disallowed;
- secrets or environment details may be exposed;
- provider payloads are outside the manual portable-surface evidence boundary.

Remediation:

- remove the payload entirely;
- package only sanitized operator feedback and necessary snippets from the manual portable-surface answer.

## Unacceptable: invented missing rating

```yaml
task_id: ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE
operator_rating_brevity_0_3: 3
packaging_note: "Rating inferred because the operator wrote that the answer was short."
```

Why blocked:

- missing ratings must not be inferred;
- qualitative notes are not a substitute for an explicit rating.

Remediation:

- set `operator_rating_brevity_0_3: NOT_PROVIDED`;
- preserve the qualitative note separately.

## Unacceptable: unsupported readiness claim

```markdown
The limited operator test validated the MVP and proves the runtime is production-ready.
```

Why blocked:

- claims validation and production readiness;
- implies runtime behavior that this manual portable-surface test cannot prove;
- violates claim boundaries.

Remediation:

- replace with: `The bundle contains sanitized limited operator feedback for import review only. It does not prove production readiness or runtime behavior.`

## Unacceptable: task ID reconstructed from memory

```yaml
task_id: probably-task-7
packaging_note: "The exact ID was missing, but this seemed like the next-lane task."
```

Why blocked:

- task IDs must be verified from approved operator notes and task materials;
- import cannot rely on memory or inference.

Remediation:

- use `task_id: BLOCKED_UNVERIFIED_TASK_ID`;
- recover the verified ID from approved operator notes or exclude the item from import.

## Unacceptable: operator-only map content

```csv
task_id,condition,raw_output_file
TASK-EXAMPLE,alpha,<operator-only-map-value>
```

Why blocked:

- operator-only maps, raw-output maps, and unblinding maps must not be packaged;
- map content can contaminate later review and exceed the portable-surface evidence boundary.

Remediation:

- remove map-derived fields;
- retain only task ID, operator feedback, sanitized snippets, and defect entries.

## Unacceptable: fake precision summary

```markdown
The manual run achieved an 87.5% pass rate and demonstrates statistically meaningful superiority.
```

Why blocked:

- computes unsupported precision from limited operator feedback;
- makes superiority and statistical claims;
- converts manual feedback into benchmark interpretation.

Remediation:

- remove calculated pass rates and superiority claims;
- present only individual operator feedback fields that were actually recorded.
