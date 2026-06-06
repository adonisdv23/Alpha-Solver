# Checks

Required checks for this implementation lane:

- focused pytest for `tests/test_local_llm_solver_orchestration_runner.py`;
- existing local LLM tests;
- standard feasible pytest subset for local LLM behavior;
- `git diff --name-only`;
- confirm no `/v1/solve` exposure was added;
- confirm no dashboard exposure was added;
- confirm no provider fallback was added;
- confirm no hosted provider call path was modified;
- confirm no real local model call was made;
- confirm no real network call was made in tests;
- confirm `behavior_evidence=false` is preserved;
- confirm unsafe or unparseable confidence cannot choose `answer_with_assumptions`;
- confirm exactly one selected next lane is recorded.

The command results are reported in the PR and final response.
