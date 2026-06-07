# Local LLM Solver Orchestration Operator Guide

## Purpose

This guide consolidates the operator documentation for the local LLM solver orchestration path after the Level 3 validation execution closeout. It is docs-only usability guidance for safely finding the approved local-only command, checking its evidence boundary, and avoiding claims or actions that the preserved Level 3 artifact does not authorize.

## Approved operator path

The approved operator-facing command identity is:

```text
python -m alpha.local_llm.operator_cli
```

Use it only as a non-production, local-only, operator-only wrapper around the existing local orchestration runner. The path is default-off, requires explicit `--enable-local-llm`, requires exactly one prompt source, requires a loopback/local endpoint, requires a local model identifier, requires a finite positive timeout, requires no hosted provider keys, and does not provide hosted or provider fallback.

## Source-of-truth packets

Use these packet paths when verifying or citing Level 3 status:

- `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/`
- `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/import-final-decision/`
- `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout/`

The closeout packet preserves the final accepted decision:

```text
LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE
```

The closeout selected next action is:

```text
NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED
```

This post-closeout operator-docs consolidation selects:

```text
NO_FURTHER_OPERATOR_DOCS_CONSOLIDATION_LANES_SELECTED
```

If this docs consolidation is found incomplete or inconsistent, use blocker fallback lane:

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-OPERATOR-DOCS-CONSOLIDATION-FIX-001
```

## Evidence boundary

The Level 3 artifact is accepted only as artifact-complete, non-promotional, local orchestration evidence. It does not establish production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, or evidence-model promotion.

This guide does not reopen validation, rerun smoke, run local models, run Ollama, call hosted providers, expose `/v1/solve`, expose dashboard routes, run benchmarks, update Google Sheets or backlog workbooks, add fallback behavior, or promote evidence.

## Start here

- Use [command-reference.md](command-reference.md) for exact safe invocation shape and required flags.
- Use [operator-safe-use-checklist.md](operator-safe-use-checklist.md) immediately before and after any local-only operator command.
- Use [level-3-validation-artifact-summary.md](level-3-validation-artifact-summary.md) to understand what the accepted Level 3 artifact did and did not establish.
- Use [evidence-boundary-quick-reference.md](evidence-boundary-quick-reference.md) before sharing, preserving, or summarizing any output.
- Use [failure-modes-and-stop-conditions.md](failure-modes-and-stop-conditions.md), [safe-use-boundaries.md](safe-use-boundaries.md), and [non-claims-and-blocked-uses.md](non-claims-and-blocked-uses.md) for legacy boundary details that remain in force.
