# EVAL-BEHAVIORAL-DEMO-001 · Expert Pass Behavioral Demo Checklist

## Purpose

Add a compact behavioral demo checklist for the opt-in OpenAI expert route so operators can review intended judgment behavior before sharing or building a preview UI.

## Scope

- Applies only to documentation and no-network checklist integrity tests.
- Covers representative prompt shapes for trivial, complex, messy or vague, clarify-needed, assumption-heavy, and block-sensitive behavior.
- References existing no-live answer-quality eval artifacts when they are present.
- Keeps provider expert-pass behavior, clarify behavior, eval artifact preservation behavior, and UI preview work unchanged.

## Success criteria

The checklist is successful when it helps an operator verify behavior shape rather than answer superiority:

- complex prompts use the expert path and expose the expert envelope;
- trivial prompts stay direct/simple and avoid unnecessary expert complexity;
- clarify-needed prompts surface clarification needs when confidence is low;
- assumption-heavy prompts surface assumptions;
- block-sensitive cases remain distinct from clarify when existing gate behavior maps very low confidence to block.

## Required artifact

Add a narrow Markdown checklist under the existing eval documentation area:

```text
docs/evals/EXPERT_PASS_BEHAVIORAL_DEMO.md
```

The checklist should include purpose, scope, prompt set, expected judgment behavior, pass/fail checks, no-network or operator-supervised run instructions, evidence artifact references, claim boundaries, and backlog impact.

## Validation expectations

Tests, if added, must be no-network and documentation-focused. They may verify that the checklist exists, contains required sections and prompt categories, references durable artifacts when present, states that it is not an answer-superiority benchmark, and includes explicit claim boundaries.

## Backlog impact

`EVAL-BEHAVIORAL-DEMO-001` should be marked Done only after the PR implementing this spec is merged. The PR should be added as implementation evidence for this lane. Backlog spreadsheets are not edited from this repo task.

## Non-goals

- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-quality superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
- No UI preview implementation.
- No provider expert-pass behavior changes.
- No clarify behavior changes.
- No eval artifact preservation behavior changes.
- No live provider tests.
- No broad eval benchmark or eval platform.
- No backlog workbook edits.
