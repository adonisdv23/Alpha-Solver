# Checks Run

The following checks were run for this docs/spec decision packet:

```bash
git status --short
```

```bash
git diff --name-only
```

```bash
git diff --check
```

```bash
find docs/local_llm_solver_orchestration_operator_cli_wrapper_decision -maxdepth 1 -type f | sort
```

```bash
rg -n "ADD_STABLE_CLI_WRAPPER|KEEP_MODULE_ENTRYPOINT_ONLY|ADD_OPERATOR_SCRIPT_TEMPLATE_ONLY|BLOCKED_REQUIRES_SPEC_OR_SURFACE_REVIEW" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

```bash
rg -n "behavior_evidence=false|no_hosted_fallback=true|no_provider_keys_required=true|/v1/solve|dashboard|provider fallback" docs/local_llm_solver_orchestration_operator_cli_wrapper_decision
```

No smoke, local model, hosted provider, API, dashboard, billing, Google Sheets, or backlog workbook command was run.
