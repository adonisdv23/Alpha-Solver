# ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001 · Post-552 No-Echo Substantive Generation Gate

## Purpose

Create a repeatable, deterministic, local-only successor gate after #552 that separates prompt echo, near echo, placeholder/stub/canned output, bounded SAFE-OUT/refusal/clarification output, and bounded substantive-derived output for synthetic fixtures with known outcomes.

## Scope

- Add a standalone checker for text outputs against prompts.
- Use synthetic fixtures only.
- Run focused local tests only.
- Produce an evidence packet under `docs/evals/runs/alpha-solver-no-echo-substantive-generation-gate-post-552-successor-001/`.
- Preserve the selected next lane:
  `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001`.

## Deterministic Categories

- `exact_prompt_echo`: normalized output exactly equals normalized prompt.
- `near_echo`: output copies too much prompt text by normalized token overlap or longest copied-span ratio.
- `placeholder_stub_canned_output`: output contains placeholder/stub/canned phrases, is too short for derived output, or lacks required answer fields.
- `safe_out_refusal_or_clarification`: output is a bounded SAFE-OUT/refusal/clarification and does not pretend to answer unsupported context.
- `substantive_derived_output`: output passes minimum length, novelty, required-field, no-placeholder, no-echo, and no-near-echo checks.

## Heuristics

- Normalize text with lowercase alphanumeric tokenization.
- `normalized_overlap_ratio`: fraction of output tokens also present in prompt tokens.
- `longest_copied_span_ratio`: longest contiguous copied prompt span divided by output token count.
- `novelty_ratio`: `1 - normalized_overlap_ratio`.
- `required_answer_fields_present`: all configured field markers appear in the output.
- `minimum derived-answer length`: default 16 output tokens.
- Placeholder/stub detection uses deterministic phrase patterns such as `placeholder`, `stub`, `TODO`, `TBD`, `coming soon`, `not implemented`, and generic-answer markers.
- SAFE-OUT/refusal/clarification detection uses deterministic bounded refusal/clarification markers, including the `SAFE-OUT:` prefix.
- SAFE-OUT/refusal/clarification markers are evaluated only after exact-echo and near-echo/copy-span checks, so those markers cannot make copied prompt text pass.

## Acceptance

- Synthetic fixtures cover exact echo, near echo, placeholder/stub/canned output, bounded SAFE-OUT/refusal/clarification, and known derived-output cases.
- Focused tests assert expected classifications and required answer-field behavior.
- The checker remains local-only and deterministic.
- Evidence packet records verdict, fixture summary, pass/fail counts, limitations, non-claims, and whether the gate alone unblocks Value Read.

## Non-goals

- No provider calls, tokens, credentials, hosted models, local model execution, external APIs, Google Sheets mutation, `/v1/solve` exposure, dashboard exposure, public API exposure, or billing behavior changes.
- No broad runtime behavior rewrite.
- No semantic-correctness, value-proof, provider-validation, model-quality, production-readiness, public-readiness, release-readiness, or Alpha-superiority claim.
- No replacement for human scoring.
