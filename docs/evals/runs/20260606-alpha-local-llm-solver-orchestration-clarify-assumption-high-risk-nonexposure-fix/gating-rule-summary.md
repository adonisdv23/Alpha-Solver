# Gating Rule Summary

The deterministic gate now applies these safety-first rules:

1. Pass-one forbidden boundary claims fail closed before normal output exposure.
2. High-risk prompt text or high-risk/non-allowlisted risk flags block before deterministic clarify or assumption overrides.
3. High-risk block outputs do not expose model-produced considerations or assumptions.
4. Underspecified prompts clarify without pass two when high-risk detection is false.
5. Pass-one `block` can become `answer_with_assumptions` only when bounded assumption answering is allowed.
6. Missing, unparseable, or low confidence cannot answer with assumptions.
7. Unsafe, unbounded, unsupported, boundary-violating assumptions, or high-risk/forbidden missing-information cues cannot answer.
8. Pass-two forbidden boundary claims fail closed and do not expose the forbidden answer.
