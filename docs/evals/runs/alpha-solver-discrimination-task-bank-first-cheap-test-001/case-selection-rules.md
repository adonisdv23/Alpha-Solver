# Case-selection rules

## Selection method

Candidate cases are selected from synthetic prompts or approved committed text references that can exercise one clear discrimination behavior at a time. Each candidate must name the case family, evidence boundary, expected allowed behavior, expected blocked behavior, and readiness status.

## Candidate count

The maximum candidate case count for this first cheap-test packet is 8 candidate cases. The recommended maximum is 8 candidate cases.

## Required evidence-boundary markers

Every candidate must include:

- `source_type`: `synthetic` or `approved_committed_text`
- `raw_outputs_included`: `false`
- `output_generation_performed`: `false`
- `scoring_performed`: `false`
- `provider_or_runtime_dependency`: `false`
- `source_map_or_unblinding_required`: `false`
- `claims_boundary`: review-only design candidate, not benchmark evidence

## Inclusion rules

Include only cases that use synthetic text or approved committed text already in the repository. Source text must be frozen by a committed reference before execution in any later lane.

## Exclusion rules

Exclude cases that require any of the following:

- current-fact prompts without a frozen source snapshot
- provider-dependent behavior
- local-model-dependent behavior
- runtime-dependent behavior
- dashboard-dependent or API-dependent behavior
- Google Sheets-dependent behavior
- private data
- raw Alpha outputs or raw baseline outputs
- score changes or scoring fields
- unblinding or source-map work

## Case-family representation

- `false_premise`: prompt includes an unsupported premise that should be corrected or bounded.
- `hidden_constraint`: prompt includes a constraint that should shape the answer even if it is easy to ignore.
- `substantive_derivation`: prompt requires reasoning from the supplied material rather than echoing it.
- `acceptable_source_use`: prompt allows concise source-grounded use without copying more than needed.
- `non_answer_safe_out`: prompt lacks enough evidence, so the allowed behavior is a bounded refusal or uncertainty statement.
- `unsupported_copying`: canonical copying failure label for copying that is not justified by the task or source boundary.
- `near_echo`: response too closely follows source structure or wording without adding required transformation.
- `paraphrase_only_response`: response rewords the source without substantive derivation.

`unsupported_copying` is the canonical copying failure label. Do not introduce `unacceptable_output_copying` as a label.
