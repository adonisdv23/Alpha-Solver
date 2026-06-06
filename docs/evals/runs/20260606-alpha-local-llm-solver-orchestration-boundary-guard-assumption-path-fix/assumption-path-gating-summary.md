# Assumption Path Gating Summary

A pass-one `block` or `answer_with_assumptions` result may proceed to pass two only when the existing bounded assumption gate is satisfied:

- confidence parses to a number and meets the configured threshold;
- considerations are present;
- assumptions are present;
- missing information is absent or bounded;
- considerations, assumptions, and missing information do not contain high-risk text or forbidden boundary terms;
- assumptions are not empty placeholders such as `none`, `n/a`, or `unknown`;
- risk flags are exact low-risk labels or benign composites made only from the narrow allowed low-risk tokens.

The Prompt 3-shaped fake-transport test covers the bounded local Python CLI startup-time planning prompt and verifies `status=ok`, `mode=answer_with_assumptions`, `pass_count=2`, and matching `answer` / `final_answer` fields.
