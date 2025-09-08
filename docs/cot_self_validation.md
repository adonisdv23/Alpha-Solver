# CoT Self-Validation

`alpha.reasoning.cot_self_validate.validate_answer` performs two deterministic
checks on Chain-of-Thought results:

* **numeric consistency** – re-evaluates simple arithmetic in the reasoning
  steps and compares against the final answer.
* **regex shape** – final answers must match at least one supplied pattern.

When validation fails and the caller's confidence is below the configured
threshold, the runner performs a single correction pass using the arithmetic
result. No randomness is introduced beyond the provided seed.
