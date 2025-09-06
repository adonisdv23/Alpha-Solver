# Local Executors

Alpha Solver includes deterministic local executors for simple math and CSV operations. These executors run without external dependencies.

## Math Evaluator

- Module: `alpha.executors.math_exec`
- Tool ID: `local.math.eval`
- Supports `+`, `-`, `*`, `/`, `**`, `%`, `//` and parentheses.

```bash
python -m alpha.executors.math_exec "2+2"
```

## CSV Operations

- Module: `alpha.executors.csv_exec`
- Tool ID: `local.csv.ops`
- Functions:
  - `row_count(path)` – count rows in a CSV file.
  - `filter_rows(path, col, value, out_path)` – write rows matching `col==value`.

Outputs are stored under `artifacts/exec/csv/<timestamp>_<name>.csv`.

## Instruction Adapter

Use `alpha.adapters.instruction_adapter.run_instruction` to dispatch JSON instructions to the executors. Each instruction is logged to `artifacts/exec/instructions.jsonl`.

Example instruction:

```json
{
  "tool_id": "local.math.eval",
  "action": "eval",
  "args": {"expr": "2+2"}
}
```
