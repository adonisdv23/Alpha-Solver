# Blocker Fallback Lane

## Fallback lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-LEVEL-3-VALIDATION-EXECUTION-AUTHORIZATION-FIX-001`

## When to use

Use this lane if this authorization decision packet is incomplete, unsafe, internally inconsistent, missing required source-evidence review, blocked, or found to have crossed an execution, local model inference, Ollama, smoke rerun, hosted provider, `/v1/solve`, dashboard, provider fallback, hosted fallback, benchmark, billing, runtime-change, source-artifact modification, frozen-packet modification, Level 2 reopening, external-ledger, or evidence-promotion boundary.

## Fallback boundary

The fallback lane must repair only the authorization packet unless a later explicit lane says otherwise. It must not execute validation or promote evidence.
