# Operator Reference Map

This map links operator-facing documentation, command references, and preserved artifacts. It does not execute any command.

| Reference type | Path | Role in traceability | Boundary |
| --- | --- | --- | --- |
| Operator guide command reference | `docs/local_llm_solver_orchestration_operator_guide/command-reference.md` | Documents operator-facing local LLM solver orchestration command usage. | Reference only; this index did not run the command. |
| Operator CLI wrapper decision | `docs/local_llm_solver_orchestration_operator_cli_wrapper_decision/` | Records why a stable local-only wrapper should exist. | Decision only. |
| Operator CLI wrapper implementation docs | `docs/local_llm_solver_orchestration_operator_cli_wrapper_implementation/` | Records wrapper implementation scope and boundaries. | No source code changed by this index. |
| Stable wrapper source reference | `alpha/local_llm/operator_cli.py` | Wrapper command identity: `python -m alpha.local_llm.operator_cli`. | Source reference only; not modified. |
| Controlled usage packet | `docs/local_llm_solver_orchestration_controlled_usage_packet/` | Defines controlled Level 2 operator usage runbook and capture template. | Packet did not execute a run. |
| Controlled usage source artifact | `docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact/` | Preserves one Level 2 controlled local operator-run artifact. | Not modified. |
| Level 3 frozen operator runbook | `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-frozen-packet/operator-runbook.md` | Freezes the Level 3 operator execution instructions used by the later source artifact. | This index did not rerun it. |
| Level 3 frozen invocation template | `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-frozen-packet/frozen-invocation-template.md` | Documents expected invocation boundaries. | Reference only. |
| Level 3 source artifact README | `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/README.md` | Describes preserved Level 3 execution artifacts. | Not modified. |
| Level 3 run metadata | `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/run_metadata.txt` | Preserves run metadata for traceability. | Not modified. |
| Level 3 captured file list | `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/file_list.txt` | Lists preserved Level 3 artifact files. | Not modified. |

## Command identity preserved

`python -m alpha.local_llm.operator_cli`

## Non-execution statement

This reference map did not run local model inference, run Ollama, rerun validation, rerun smoke, call hosted providers, expose or call `/v1/solve`, expose or call dashboard routes, add provider fallback, add hosted fallback, run benchmarks, perform billing work, update Google Sheets, update backlog workbooks, or promote evidence.
