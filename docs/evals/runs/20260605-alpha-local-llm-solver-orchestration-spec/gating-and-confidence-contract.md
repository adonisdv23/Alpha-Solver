# Gating and Confidence Contract

## Gate modes

The local orchestration runner must choose exactly one mode:

- `direct`;
- `clarify`;
- `answer_with_assumptions`;
- `block`.

## Confidence handling

Confidence is a local orchestration signal only. It is not model-quality evidence, benchmark evidence, production-readiness evidence, or MVP validation.

If Pass 1 confidence cannot be parsed safely, or if Pass 1 output is unsafe, empty, echoed, malformed, or ambiguous, the runner must not choose `direct` or `answer_with_assumptions`. It must fail closed, clarify, or block.

If confidence is parsed safely but material information is missing, the runner may choose `answer_with_assumptions` only when assumptions are explicit, bounded, low-risk, and supported by parsed considerations. Otherwise it must clarify, block, or fail closed.

## Boundary

Gating and confidence must not promote `behavior_evidence` to true and must not create `/v1/solve` or dashboard exposure.
