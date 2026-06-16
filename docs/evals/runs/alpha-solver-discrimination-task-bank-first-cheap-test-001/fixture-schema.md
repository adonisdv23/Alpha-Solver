# Fixture schema

Future fixtures must use only synthetic text or approved committed text. This schema is a design structure only and is not an execution artifact.

## Required fields

```yaml
fixture_id: string
prompt: string
source_text: string | null
frozen_source_reference: string
expected_capability_target: string
expected_allowed_answer_behavior: string
expected_blocked_behavior: string
expected_no_echo_requirement: string
expected_classification_label_set:
  - exact_echo
  - near_echo
  - paraphrase_only_response
  - substantive_derivation
  - acceptable_source_use
  - unsupported_copying
  - non_answer_safe_out
evidence_boundary:
  source_type: synthetic | approved_committed_text
  raw_outputs_included: false
  output_generation_performed: false
  scoring_performed: false
  provider_or_runtime_dependency: false
  source_map_or_unblinding_required: false
non_claims:
  - no Alpha superiority claim
  - no benchmark success claim
  - no value or readiness claim
  - no provider, local-model, runtime, dashboard, public API, /v1/solve, Google Sheets, production, public, or security/privacy validation claim
review_notes: string
```

## Field notes

- `fixture_id`: stable identifier for the future fixture.
- `prompt`: the exact prompt to freeze in a later authorized fixture lane.
- `source_text`: synthetic or approved committed source text when distinct from the prompt.
- `frozen_source_reference`: committed path or synthetic packet reference that can be audited without raw outputs.
- `expected_capability_target`: one narrow capability under review.
- `expected_allowed_answer_behavior`: behavior a reviewer may treat as allowed if later outputs are generated under authorization.
- `expected_blocked_behavior`: behavior a reviewer should treat as blocked.
- `expected_no_echo_requirement`: no exact echo, no near echo unless explicitly allowed for minimal citation, and no paraphrase-only response when substantive derivation is required.
- `expected_classification_label_set`: closed label vocabulary for this packet.
- `evidence_boundary`: confirms that no raw outputs, scoring, provider/runtime dependency, source-map work, or unblinding is included.
- `non_claims`: explicit claim boundary for each future fixture.
- `review_notes`: operator notes for clarity issues, rewrite needs, or exclusion.

Do not include `unacceptable_output_copying` as a label.
