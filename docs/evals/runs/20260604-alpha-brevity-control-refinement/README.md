# Alpha Brevity Control Refinement

Lane ID: `ALPHA-BREVITY-CONTROL-REFINEMENT-001`

## Objective

Refine the minimal portable Alpha behavior contract so it remains useful on higher-headroom tasks while reducing unnecessary expansion on concise, reviewer-facing, low-headroom, or answer-first prompts.

## Source interpretation

This lane consumes PR #270's final decision: `Refine current contract`.

PR #270 interpreted the post-improvement result as Alpha 314 / Plain 303 / Alpha-minus-plain +11, with Alpha wins 5, Plain wins 1, and 2 ties. The interpretation classified the result as `B. Mixed improvement with brevity/control concern`, supporting a narrow contract refinement rather than broad runtime, production, or superiority claims.

## Files changed

- `alpha_solver_portable.py`
- `tests/test_alpha_minimal_behavior_contract.py`
- `docs/evals/runs/20260604-alpha-brevity-control-refinement/README.md`

## What changed

- Strengthened answer-first wording for direct answers, concise rewrites, direct extractions, short confirmations, and next actions.
- Added low-headroom restraint wording for simple rewrites, formatting, reviewer-facing edits, and one-step admin tasks.
- Resolved the envelope-vs-low-headroom conflict by adding a compact-envelope / minimal-section mode: low-headroom tasks keep SolverEnvelope labels while allowing non-essential sections such as EXPERT TEAM and SHORTLIST to stay minimal, with default expanded counts applying only outside compact-envelope mode.
- Added compact caveat and task-relevant risk wording to suppress generic risk boilerplate while preserving truthful uncertainty and claim boundaries.
- Kept artifact stop conditions, evidence-boundary behavior, and safe claim wording intact.

## What did not change

- No capture run.
- No scoring or rescoring.
- No unblinding.
- No Google Sheets update.
- No Batch C materials.
- No runtime API, provider adapter, model configuration, routing, or `/v1/solve` behavior changes; compact-envelope mode is portable prompt-contract wording only.
- No provider calls.
- No scored artifacts, raw outputs, sanitized scorer-facing packets, or operator maps changed.

## Non-claims

This refinement does not claim MVP validation, broad Alpha superiority, broad plain-provider inferiority, production readiness, benchmark success, exact billing accuracy, runtime readiness, provider orchestration, self-healing, adaptive learning, self-optimization, autonomous optimization, `/v1/solve` behavior, runtime API behavior, provider behavior, or model routing behavior.

## Recommended future validation step

Recommended next validation lane: run a narrow offline portable-surface validation for answer-first, brevity/control, compact caveats, and preservation of claim-boundary and artifact-discipline behavior before considering any broader measurement lane.
