# Acceptable Evidence Examples

Standard ID: `ALPHA-LIMITED-OPERATOR-TEST-EVIDENCE-PACKAGING-STANDARD-001`

Status: examples use synthetic placeholders only. They are not actual operator-test results.

## Example 1: import-ready task evidence row

```yaml
task_id: ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE
task_family: concise reviewer comment
operator_name: <approved-operator-name-or-pseudonym>
test_date: <YYYY-MM-DD>
test_surface: portable Alpha behavior contract only
portable_surface_context: manual paste into approved portable-surface prompt context
stop_condition_reached_yes_no: no
stop_condition_id_or_summary: NOT_APPLICABLE
operator_rating_direct_usefulness_0_3: <operator-entered-0-3>
operator_rating_brevity_0_3: <operator-entered-0-3>
operator_rating_answer_first_0_3: <operator-entered-0-3>
operator_rating_claim_boundary_0_3: <operator-entered-0-3>
operator_rating_evidence_boundary_0_3: <operator-entered-0-3>
operator_rating_next_action_0_3: <operator-entered-0-3>
overall_operator_rating_0_3: <operator-entered-0-3>
keep_refine_reject: <operator-entered-keep-refine-reject>
primary_defect: <operator-entered-defect-or-NOT_PROVIDED>
notes: <sanitized operator note copied from an actual manual run>
```

Why acceptable:

- cites a task ID;
- identifies the portable test surface;
- uses placeholders showing where actual operator-entered integer ratings would be copied;
- avoids private data, raw payloads, full transcript text, benchmark claims, and readiness claims;
- preserves operator feedback as feedback only.

## Example 2: sanitized response snippet supporting a defect

```yaml
task_id: ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE
snippet_type: sanitized_response_snippet
supports: defect evidence for unsupported claim
snippet: "The response stated that the lane was '[BLOCKED_UNSUPPORTED_CLAIM]' even though the prompt provided no evidence for that status."
redactions:
  - marker: "[BLOCKED_UNSUPPORTED_CLAIM]"
    reason: unsupported readiness wording removed from packaged snippet
```

Why acceptable:

- includes only the minimal relevant excerpt;
- labels the evidence as a snippet, not a transcript;
- ties the snippet to one task ID;
- avoids exposing a full response;
- flags unsupported claim language rather than endorsing it.

## Example 3: preserved operator note with private organization redacted

```yaml
task_id: ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE
operator_note: "The answer invented a release date for [REDACTED_PRIVATE_ORG] and should trigger the invented status defect type."
packaging_note: "Private organization name redacted; operator meaning preserved."
```

Why acceptable:

- preserves the defect observation;
- removes the private organization name;
- does not invent a replacement organization;
- does not turn the note into validation or scoring interpretation.

## Example 4: missing field marked honestly

```yaml
task_id: ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE
operator_rating_brevity_0_3: NOT_PROVIDED
notes: "Operator provided qualitative notes but left the brevity rating blank."
bundle_status: blocked until importer decides whether to import the qualitative note without the missing rating
```

Why acceptable:

- does not fabricate a rating;
- marks the field with an approved missing-field marker;
- makes the import limitation explicit.

## Example 5: redaction log entry

| task_id | evidence_item | redaction_marker | reason | meaning_preserved_yes_no | reviewer_note |
| --- | --- | --- | --- | --- | --- |
| `ALPHA-LIMITED-OPERATOR-TEST-001-TASK-EXAMPLE` | `operator_note` | `[REDACTED_PRIVATE_URL]` | private ticket URL removed | yes | note still supports raw-output boundary concern |

Why acceptable:

- records what category was redacted;
- does not reveal the private URL;
- indicates whether review meaning remains intact.
