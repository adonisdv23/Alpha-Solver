# Frozen Batch C Prompt Packet

Lane ID: `ALPHA-BATCH-C-FROZEN-PACKET-PREP-001`

## Packet status

This is the frozen Batch C prompt-contract simulation packet. After this file is committed, future manual execution must use the task set exactly as recorded in `batch-c-task-set.md`, unless a later approved docs lane creates a new frozen packet.

## What is frozen

- The task IDs, order, prompts, and scoring intent in `batch-c-task-set.md`.
- The operator capture requirements in `operator-runbook.md` and `raw-artifact-capture-template.md`.
- The feedback, scorer-facing sanitization, and import scaffolds in this folder.
- The residual-risk and claim-boundary language in this folder.

## Portable prompt-contract behavior boundary

Batch C is designed only to exercise the current portable prompt-contract behavior boundary from `alpha_solver_portable.py`:

- Direct answer first for yes/no, short rewrite, reviewer comment, extraction, short confirmation, and next-action tasks.
- Low-headroom restraint for simple rewrite, formatting, extraction, confirmation, reviewer-facing edit, and one-step admin tasks.
- Requested answer shape before added structure.
- No invented owners, dates, file paths, commands, metrics, acceptance criteria, implementation status, provider-side claims, or operational artifacts.
- Compact caveats that preserve uncertainty, safety, evidence limits, and claim boundaries.
- Risk discussion only when it changes the next action or protects artifact integrity.
- Limited-evidence wording only; no broad comparative, MVP, production, benchmark, billing, runtime, endpoint, provider-orchestration, or local-model quality claims.
- Repository evidence controls over external planning ledgers.
- Output-format contamination guard for reviewer comments, replacement wording, checklists, status updates, and compact prompt/template tasks.
- Artifact stop conditions when required score tables, capture packets, or raw artifacts are absent.

## Batch C operator setup

1. Use a clean manual prompt-contract simulation context.
2. Load the current portable prompt-contract instructions according to the operator-approved procedure.
3. Run only the frozen tasks in `batch-c-task-set.md`, in order.
4. Preserve each raw output before any scoring, cleanup, redaction, or summary.
5. Do not rerun a task after viewing an output unless a later approved protocol explicitly authorizes a replacement attempt.
6. Record any execution anomaly in the raw capture template without editing the raw output.

## Required operator artifacts for a future run

A future operator run must produce all of the following before any results import:

- One raw artifact capture entry per task.
- One operator feedback entry per task.
- One scorer-facing sanitization entry per task.
- A redaction log showing what was removed or replaced.
- A preservation checklist completed by the operator.
- A reviewer checklist completed before import.

## Explicit non-execution statement

This PR prepares the frozen packet only. It does not execute Batch C, capture Batch C outputs, score outputs, import results, interpret results, or update Google Sheets.
