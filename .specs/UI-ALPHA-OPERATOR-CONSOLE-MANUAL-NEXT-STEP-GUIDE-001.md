# UI-ALPHA-OPERATOR-CONSOLE-MANUAL-NEXT-STEP-GUIDE-001 · Operator Console Manual Next Step Guide

Lane id: `AOC-B008A-OPERATOR-NEXT-STEP-CLARITY-001`

## Goal

Add a compact, protected Operator Console card and status payload section named `manual_next_step_guide` that helps an operator distinguish:

1. what can be reviewed now,
2. what can only happen manually outside the console, and
3. what remains blocked inside the console.

This lane is a clarity lane, not an action queue.

## Motivation

The Operator Console already exposes local artifact summaries, freshness metadata, provider/cost gate status, a display-only dry-run preview, local receipt metadata, and manual ChatGPT copy/paste guidance. Operators need a small safety-oriented guide that ties those surfaces together without creating action semantics or execution affordances.

## Scope

- Add a display-only `Manual Next Step Guide` status section.
- Render a page card under `/dashboard/operator-console`.
- Use bounded labels only: `label`, `section`, `status`, `description`, `source_surface`, and `boundary`.
- Include exactly these user-facing sections:
  - `Available for review`
  - `Manual-only steps`
  - `Blocked in this console`
- Derive meaning only from existing safe surfaces and fixed boundary copy.
- Keep the existing Local Receipt Store as the only controlled write action.

## Non-goals

- No action queue, task queue, job queue, queue persistence, processor, or workbench behavior.
- No runner, scheduler, worker, dispatch, approval, retry, or action-control behavior.
- No dry-run execution, live-provider execution, ChatGPT API integration, browser automation, `/v1/solve` invocation, CLI/subprocess execution, or prompt submission.
- No paste textarea, paste storage, capture editor, raw prompt viewer, raw output viewer, or raw route metadata viewer.
- No new POST route, new local persistence model, general-purpose file writing, user-supplied path handling, credential validation, provider ping, or schema migration.
- No readiness, validation, benchmark, production, scoring, ranking, winner, or superiority claim.

## Code targets

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/INDEX.md`

## Tests

Focused tests must prove:

- Status JSON includes `manual_next_step_guide`.
- The page renders a `Manual Next Step Guide` card.
- The card includes the three required sections.
- The card states the display-only and non-executing boundary.
- The card has no buttons, forms, textareas, or new action controls.
- No new Operator Console POST route exists beyond the receipt route.
- The existing receipt route remains the only controlled write action.
- Raw prompts, raw outputs, raw route metadata, provider payloads, secrets, and pasted model output are not surfaced.
- Provider/cost gate, dry-run preview, ChatGPT copy/paste capture, live-run disabled state, and route/trace placeholders remain bounded.
- Process-hardening guards still pass for page and status rendering.

## Definition of done

- `manual_next_step_guide` appears in the status JSON with bounded summary fields only.
- The protected Operator Console page shows a compact `Manual Next Step Guide` card.
- The card has no new button and no new write or execution behavior.
- Focused and broad Operator Console tests pass.
- Documentation explains the panel and its boundaries.

## Boundary checklist

- [x] Display-only clarity panel.
- [x] No provider calls.
- [x] No ChatGPT calls.
- [x] No `/v1/solve` calls.
- [x] No browser automation.
- [x] No CLI, shell, or subprocess execution.
- [x] No prompt submission.
- [x] No paste storage.
- [x] No capture editor.
- [x] No raw prompt/output display.
- [x] No new POST route.
- [x] No new write path.
- [x] Local Receipt Store remains the only controlled write path.
- [x] No user-supplied path or filename handling.

## Non-claims

The guide does not claim readiness, validation, benchmark performance, production suitability, scoring, ranking, winner selection, superiority, billing accuracy, provider availability, or output quality.
