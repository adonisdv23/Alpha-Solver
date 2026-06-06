# Gating Rule Summary

Pass-one gate behavior after this fix:

1. `block` returned by pass one remains terminal.
2. Explicit high-risk prompt text or high-risk risk flags force `block`.
3. Deterministically underspecified prompts force `clarify` unless a safety block already applied.
4. `direct` requires safely parsed confidence and no missing-information entries, but does not require considerations.
5. `answer_with_assumptions` requires safely parsed confidence, bounded assumptions, supporting considerations, and no unbounded or unsafe assumption text.
6. Ordinary optimization, implementation, profiling, latency, performance, and unknown risk flags do not automatically block low-risk execution-planning tasks.

These are deterministic runner rules, not model-quality assertions.
