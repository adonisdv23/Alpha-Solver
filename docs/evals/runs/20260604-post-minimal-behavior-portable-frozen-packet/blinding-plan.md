# Blinding Plan

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: future blinding plan only, pre-capture and pre-scoring.

## Randomized assignment

During a later authorized capture task, assign Output A and Output B randomly per prompt after both condition outputs are preserved.

Randomization must be recorded in the operator-only map. The assignment may vary by comparison; do not use a visible repeating pattern.

This packet does not create actual A/B assignments.

## Scorer-facing sanitization

Before blind scoring, build the scorer-facing packet from a sanitized render, not directly from the raw output files. Raw output files remain exact preservation artifacts; the sanitized render is a separate blind-scoring artifact.

Sanitization must follow `docs/evals/BLIND_SCORING_PROCEDURE.md`. It may neutralize direct brand, provider, route, condition, heading, footer, and envelope tells while preserving the substance of the answer. It must not remove caveats, reasoning, risks, assumptions, recommendations, omissions, verbosity, contradictions, or other answer-quality defects.

Apply sanitization symmetrically to both outputs. If direct tells cannot be removed without substantive rewriting, stop before scoring and regenerate the scorer-facing packet from a clean sanitized render.

## Scorer-facing packet contents

The scorer-facing packet must contain only:

- comparison ID;
- prompt ID;
- prompt text;
- blinded Output A;
- blinded Output B;
- scorer instructions and score fields.

## Scorer-facing exclusions

The scorer-facing packet must not contain:

- Alpha Solver names;
- Alpha/plain labels;
- portable-contract labels;
- provider/model labels;
- route identity;
- run timestamps;
- runtime notes;
- repo paths;
- assignment patterns;
- raw output paths;
- pipeline confirmation branding;
- condition-identifying headings or footers;
- operator notes;
- unblinding maps or unblinding-map details;
- prior eval outcomes;
- rubric changes or new rubric semantics.

## Operator-only map

The operator-only map must be preserved separately from scorer-facing material. It must not be opened, summarized, applied, or sent to the scorer until blind scoring is complete and unblinding is separately authorized.

## Scorer non-inference instruction

The scorer must be instructed not to infer condition identity from tone, structure, length, formatting, route-like language, envelope shape, or any other cue. The scorer must use only the visible Output A and Output B content.

## Unblinding rule

Unblinding happens only after blind scoring is complete, preserved, validated for completeness, and separately authorized. If the scorer-facing packet contains direct condition labels, Alpha Solver branding, provider/model branding, route identity, runtime metadata, repo paths, raw output paths, pipeline confirmation branding, or unblinding-map details, stop before scoring and regenerate the sanitized scorer-facing packet.
