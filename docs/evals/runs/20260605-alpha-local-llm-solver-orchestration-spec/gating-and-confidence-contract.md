# Gating and Confidence Contract

## Gate modes

The local orchestration runner must choose exactly one mode:

- `direct`;
- `clarify`;
- `answer_with_assumptions`;
- `block`.

## Confidence handling

Confidence is a local orchestration signal only. It is not model-quality evidence, benchmark evidence, production-readiness evidence, or MVP validation.

If confidence cannot be parsed safely or if missing information is material, the runner must prefer `clarify`, `answer_with_assumptions`, `block`, or fail-closed behavior rather than presenting unsupported local output as a successful answer.

## Boundary

Gating and confidence must not promote `behavior_evidence` to true and must not create `/v1/solve` or dashboard exposure.
