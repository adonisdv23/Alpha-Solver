# Test Summary

Focused tests were added or updated in `tests/test_local_llm_solver_orchestration_runner.py` using fake or sequenced transports only.

Covered behavior:

- Prompt 3-shaped bounded local Python CLI startup-time planning prompt reaches `answer_with_assumptions`.
- Benign composite low-risk flags can proceed only when bounded assumption requirements are satisfied.
- Composite flags with high-risk tokens block without a pass-two call.
- Unknown non-allowlisted risk flags block without a pass-two call.
- Prompt 5-style pass-one boundary guard blocks forbidden fields without exposing normal output.
- High-risk prompt non-exposure remains preserved.
- Existing local-only and compatibility invariants remain covered.

No local model calls, hosted provider calls, network calls, smoke rerun, source artifact import, or Google Sheets update were performed.

## PR #342 correction tests

Additional fake-transport coverage verifies that mixed negated and positive pass-one boundary claims in one field fail closed without exposure, while a negated disclaimer-only field can proceed when the bounded assumption gate is otherwise satisfied.
