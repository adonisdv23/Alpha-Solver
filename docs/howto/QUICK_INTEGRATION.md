# Quick Integration

Use the Alpha Solver components in your application:

1. Install package and set up environment.
2. Fetch a token or API key if required.
3. Call the solver utilities.

Example using the local math evaluator:

```python
from alpha.executors.math_exec import evaluate
print(evaluate("1+2")["result"])
```

Run the CLI for help on available flags:

```bash
python alpha_solver_cli.py --help
```
