# Heuristic Spec

## Purpose

Describe review aids for identifying echo, near echo, safe non-answers, and substantive transformation. These heuristics are review aids, not proof of quality.

## Normalization

A future static checker may normalize text by lowercasing, tokenizing alphanumeric terms, removing repeated whitespace, and preserving stable IDs as tokens.

## Overlap ratio

`overlap_ratio = copied_or_shared_output_tokens / output_tokens`

Use the ratio to flag output that relies heavily on prompt or source tokens. The ratio should be interpreted with copied-span checks and source-use allowances because short required IDs can inflate overlap.

## Copied-span ratio

`copied_span_ratio = longest_contiguous_source_span_in_output / output_tokens`

Use this to catch near echo even when the total overlap ratio is diluted by a preface or closing sentence.

## Added-reasoning markers

Potential markers of added reasoning include:

- `because`, `therefore`, `so`, `this implies`, `the constraint is`, `the risk is`, `the safe next step is`;
- explicit classification labels tied to source evidence;
- decision rules or stop conditions derived from source text;
- bounded implications that do not introduce unsupported external facts.

These markers are not sufficient by themselves. A copied response with `because` can still fail.

## Source-preserving but transformed answer markers

Acceptable transformed answers may preserve:

- stable lane IDs;
- status tokens;
- file paths;
- short quoted snippets when requested;
- exact labels needed for traceability.

They should add reviewable transformation, such as mapping a status to an allowed action, separating evidence from non-claims, or converting a risk into a stop condition.

## Non-answer safe-out markers

A non-answer safe-out may include:

- `SAFE-OUT:`;
- `blocked`;
- `cannot determine from the provided evidence`;
- `operator review required`;
- `insufficient evidence`;
- `clarification required`.

Safe-out markers must not override exact echo, near echo, or unsupported copying findings. Apply copying checks first.

## Proof boundary

Passing heuristic thresholds would not prove answer quality, semantic correctness, model capability, provider behavior, local-model behavior, value, readiness, benchmark success, production suitability, public API suitability, or Alpha superiority. Heuristics only support consistent review triage.
