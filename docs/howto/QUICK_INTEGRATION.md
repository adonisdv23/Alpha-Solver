# Quick Integration

Call Alpha Solver from your application:

```python
from alpha_solver_entry import _tree_of_thought

def solve(question: str) -> str:
    """Return the final answer from Alpha Solver."""
    return _tree_of_thought(question)["final_answer"]
```

For CLI usage run:

```bash
python alpha_solver_cli.py --help
```
