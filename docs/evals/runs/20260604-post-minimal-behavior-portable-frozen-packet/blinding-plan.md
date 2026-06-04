# Blinding Plan

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: future blinding plan only, pre-capture and pre-scoring.

## Randomized assignment

During a later authorized capture task, assign Output A and Output B randomly per prompt after both condition outputs are preserved.

Randomization must be recorded in the operator-only map. The assignment may vary by comparison; do not use a visible repeating pattern.

This packet does not create actual A/B assignments.

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

- Alpha/plain labels;
- provider identity;
- model metadata;
- run timestamps;
- runtime notes;
- repo paths;
- assignment patterns;
- raw output file paths;
- operator notes;
- unblinding maps;
- prior eval outcomes;
- rubric changes or new rubric semantics.

## Operator-only map

The operator-only map must be preserved separately from scorer-facing material. It must not be opened, summarized, applied, or sent to the scorer until blind scoring is complete and unblinding is separately authorized.

## Scorer non-inference instruction

The scorer must be instructed not to infer condition identity from tone, structure, length, formatting, route-like language, envelope shape, or any other cue. The scorer must use only the visible Output A and Output B content.

## Unblinding rule

Unblinding happens only after blind scoring is complete, preserved, validated for completeness, and separately authorized. If the scorer-facing packet leaks identity or assignment information, stop and regenerate a clean blinded packet before scoring.
