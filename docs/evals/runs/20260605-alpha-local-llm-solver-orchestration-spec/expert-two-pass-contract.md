# Expert Two-Pass Contract

## First quality-lift feature

Local expert two-pass is the first quality-lift feature selected for implementation.

## Pass 1

Pass 1 asks the local LLM to extract:

- considerations;
- assumptions;
- confidence;
- missing-information or uncertainty notes where available.

## Deterministic parse

The runner must parse Pass 1 deterministically:

1. parse JSON when valid JSON is available;
2. fall back to conservative section parsing only when the section structure is safe and bounded;
3. fail closed, clarify, or block when parsing is unsafe, empty, echoed, malformed, or ambiguous.

## Gate

The runner must choose exactly one gate mode:

- `direct`;
- `clarify`;
- `answer_with_assumptions`;
- `block`.

## Pass 2

Pass 2 asks the local LLM to answer using the parsed considerations and assumptions. Pass 2 must preserve default-off, explicit opt-in, localhost-only, no-provider-key, finite-timeout, no-hosted-fallback, and `behavior_evidence=false` behavior.

## Output

The normalized Alpha-style result must include answer, considerations, assumptions, confidence, mode, metadata, and evidence boundary.
