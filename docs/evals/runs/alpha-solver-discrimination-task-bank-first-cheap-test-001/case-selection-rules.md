# Case-selection rules

## Controlling taxonomy

The first cheap-test packet is controlled by the prior discrimination task-bank asset taxonomy. It drafts exactly five representative task cards, one for each taxonomy family:

1. `false-premise`
2. `hidden-constraint`
3. `should-stop`
4. `confidence`
5. `claim-boundary`

Derivation / no-echo labels may be used as review labels or failure-mode labels, but they do not replace the five task-bank taxonomy families.

## Selection method

Task cards are selected from synthetic prompts or approved committed text references that can exercise one taxonomy family at a time. Each task card must name the taxonomy family, prompt or source sketch, reason for inclusion, expected allowed behavior, expected blocked behavior, evidence boundary, readiness status, and applicable review labels.

## Task-card count

This first cheap-test packet must contain exactly 5 representative task cards. The maximum task-card count is 5, one per required taxonomy family.

## Required evidence-boundary markers

Every task card must include:

- `source_type`: `synthetic` or `approved_committed_text`
- `raw_outputs_included`: `false`
- `output_generation_performed`: `false`
- `scoring_performed`: `false`
- `provider_or_runtime_dependency`: `false`
- `source_map_or_unblinding_required`: `false`
- `claims_boundary`: review-only task-card design, not benchmark evidence

## Inclusion rules

Include only task cards that use synthetic text or approved committed text already in the repository. Source text must be frozen by a committed reference before execution in any later lane.

## Exclusion rules

Exclude task cards that require any of the following:

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

## Taxonomy-family representation

- `false-premise`: the task asks the answerer to handle an unsupported or misleading premise without accepting it.
- `hidden-constraint`: the task includes a constraint that must govern the answer even if it is easy to miss.
- `should-stop`: the task lacks enough evidence or authorization, so the expected behavior is to stop, safe out, or request review.
- `confidence`: the task requires bounded confidence, uncertainty handling, and evidence-gap disclosure.
- `claim-boundary`: the task requires safe wording that avoids broad value, readiness, benchmark, provider, local-model, production, public, security/privacy, partnership, Pi.dev integration, external-use approval, buyer-validation, traction, or Alpha-superiority claims.

## Review-label usage

The following derivation / no-echo labels may be attached as review labels or failure-mode labels where relevant:

- `exact_echo`
- `near_echo`
- `paraphrase_only_response`
- `substantive_derivation`
- `acceptable_source_use`
- `unsupported_copying`
- `non_answer_safe_out`

`unsupported_copying` is the canonical copying failure label. Do not introduce `unacceptable_output_copying` as a label.
