# Simulation Run Record

STATUS: NOT RUN - PROMPT-CONTRACT SIMULATION TEMPLATE ONLY.

Lane ID: `ALPHA-SOLVER-MANUAL-DISCRIMINATION-VALUE-READ-001`

Track: `S` - simulation/no-provider.

## Boundary

This track is reserved for comparing the Alpha portable prompt-contract against a plain baseline prompt using the same no-provider model if available. It must be labeled prompt-contract simulation only. It must not be mixed with runtime/provider evidence.

No simulation outputs were generated in this commit. This packet preserves the task bank, prompts, scoring sheets, and boundaries for an operator-run simulation.

## Contract source reviewed

- `alpha_solver_portable.py`
- Portable version observed in source: `2.3.0-P3-PORTABLE-SPEC`
- Relevant behavior: portable spec requires SolverEnvelope-shaped responses and evidence-bound, caveated behavior; this lane adds a discrimination envelope for the Alpha-side answer during this manual value read.

## Alpha simulation system prompt template

```text
You are Alpha Solver v2.3.0-P3, running in PORTABLE-SPEC mode.
Use the portable prompt-contract behavior from alpha_solver_portable.py.
For this manual discrimination value-read task only, every Alpha-side answer must include this exact machine-checkable output envelope with these snake_case field names:
answerability_verdict: answerable, underspecified, false premise, hidden constraint, unsafe/edge, needs human, or blocked
confidence_level: low, medium, high
assumptions_detected:
missing_evidence:
would_change_if_conditions:
will_not_claim:
needs_human_escalation_reason: if applicable; otherwise `not applicable`
next_safe_operator_action:
Answer the user task without inventing evidence. Keep ordinary control tasks proportionate and avoid over-triggering. Do not rename, space-separate, title-case, or omit these contract field names.
```

## Plain baseline prompt template

```text
Answer the following user request helpfully and concisely. Do not use special Alpha Solver formatting.
```

## Per-task capture template

For each task in `task-bank.md`, preserve:

```text
Task ID:
Condition: Alpha simulation | Plain baseline
Model/tool used:
Date/time UTC:
Prompt sent:
Raw output:
Blinded output ID:
Notes on redaction or formatting normalization:
```

## Current tally

No Track S outputs were generated or scored in this commit.

Simulation tally: `not run / no scores`.
