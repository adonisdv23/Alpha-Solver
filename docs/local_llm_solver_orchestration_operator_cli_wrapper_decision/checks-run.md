# Checks Run

The following checks were run for this docs/spec decision packet update:

```bash
git diff --name-only
```

```bash
git diff --check
```

```bash
git diff --name-only | rg -v '^docs/local_llm_solver_orchestration_operator_cli_wrapper_decision/' || true
```

```bash
rg -n "not required or accepted|required or accepted" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

```bash
rg -n "hosted-provider-key CLI flags|credential inputs|command arguments" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

```bash
rg -n "environment variables must not affect|environment variables must not change|allow hosted-provider-key environment variables" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

```bash
rg -n "fail-closed provider-key rejection|fail-closed behavior|fail-closed rejection" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

```bash
git diff --name-only | rg '^(alpha/|tests/|api/|dashboard/)' || true
```

No smoke, local model, hosted provider, API, dashboard, billing, Google Sheets, or backlog workbook command was run.
