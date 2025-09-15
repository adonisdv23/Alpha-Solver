# Alpha Solver CLI

The command line tool `alpha-solver` wraps core solver features for offline use.
Source completion support is available via `source cli/completion.sh`.

## Quickstart

```bash
python cli/alpha_solver_cli.py --help
```

## Commands

### run
Solve a prompt from stdin or `--file` and print a compact **Obs Card**.

```bash
echo "hello world" | python cli/alpha_solver_cli.py run
python cli/alpha_solver_cli.py run --file prompt.txt --out json
```

### replay
Replay a JSONL record and report determinism.

```bash
python cli/alpha_solver_cli.py replay record.jsonl
```

### gates
Show gate thresholds and evaluate a sample.

```bash
python cli/alpha_solver_cli.py gates --confidence 0.3 --tokens 10
```

### finops
Estimate token usage and cost for a sample.

```bash
python cli/alpha_solver_cli.py finops --prompt "hi there" --min-budget-tokens 10
```

### traces
Run with tracing enabled and print a trace-id.

```bash
python cli/alpha_solver_cli.py traces --prompt "hi"
```
