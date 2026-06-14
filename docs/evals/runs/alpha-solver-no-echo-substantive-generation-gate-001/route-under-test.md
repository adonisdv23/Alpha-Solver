# Route Under Test

STATUS: BLOCKED - ALPHA PATH ECHOES PROMPT.

Lane ID: `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-001`

## Identified Alpha path

The local Alpha path tested was:

```text
alpha_solver_entry._tree_of_thought(prompt, enable_cache=False)
  -> alpha-solver-v91-python.py::_tree_of_thought(...)
  -> alpha.solver.observability.AlphaSolver.solve(...)
  -> alpha.reasoning.tot.TreeOfThoughtSolver.solve(...)
  -> alpha.policy.safe_out_sm.SafeOutStateMachine.run(...)
  -> user-visible envelope fields: solution / final_answer
```

This path was selected because:

- `alpha_solver_entry.py` is the importable repository entrypoint and loads `alpha-solver-v91-python.py`.
- `alpha-solver-v91-python.py` exposes `_tree_of_thought` and `AlphaSolver`.
- The value experiment protocol requires the Alpha condition to use the actual Alpha path intended for product evaluation, not a deterministic echo path, placeholder path, canned-output path, or stub path.
- The portable monolith is a portable spec/prompt contract and explicitly identifies its deterministic reasoning core as a stub, so it was inspected but not selected as sufficient value-experiment runtime proof.

## Provider boundary

No provider route was invoked. No provider credentials, tokens, live APIs, or eval execution were used.
