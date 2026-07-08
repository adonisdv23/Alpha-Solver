# UI-ALPHA-OPERATOR-CONSOLE-DAILY-USE-WALKTHROUGH-001 · Operator Console Daily-Use Walkthrough

Lane id: `AOC-DAILY-USE-WALKTHROUGH-001`

## Goal

Add a short, reproducible manual walkthrough that lets an Alpha Solver operator use the current protected Operator Console and the First 5 Minutes docs in a daily-use sequence.

This is a docs/process lane only. It makes operator confusion visible before any future UI, intent-review, dry-run, provider, or automation lane is considered. It does not change code, UI, routes, write paths, or execution behavior.

## Scope

- Add an `Operator Console Daily-Use Walkthrough` section to `docs/OPERATOR_CONSOLE.md` near the existing First 5 Minutes onboarding section.
- Explain that the walkthrough is a manual operator comprehension check, not a runner and not proof of answer quality.
- Include a 5 to 10 minute time box.
- List prerequisites for using the protected local-first console.
- Provide an ordered operator checklist for the current console surfaces:
  - protected `/dashboard/operator-console` page
  - local-first and provider-disabled header language
  - First 5 Minutes checklist
  - Local Artifact Status
  - Freshness and Sequence Coherence
  - Provider, Model, and Cost Gate
  - Dry-Run Preview
  - Manual Next Step Guide
  - ChatGPT Copy/Paste Capture
  - Local Receipt decision
  - blocked provider, ChatGPT, `/v1/solve`, command, capture-edit, and paste-storage behavior
  - first confusion point
- List expected operator-understanding outcomes.
- List failure signals that may show future docs or UI refinement is needed.
- Provide a copyable manual notes template that is filled out outside the console.
- State explicit non-claims for answer quality, route correctness, model superiority, provider readiness, billing accuracy, benchmark validity, production readiness, validation success, and execution safety beyond the currently documented console boundaries.

## Non-goals

- No new Operator Console UI.
- No new card.
- No new status key.
- No new endpoint.
- No new POST route.
- No new receipt behavior.
- No new write path.
- No provider execution.
- No ChatGPT API integration.
- No browser automation.
- No `/v1/solve` invocation.
- No CLI, subprocess, shell, or command execution from the console.
- No dry-run execution.
- No paste storage.
- No capture editor.
- No raw prompt or raw output viewer.
- No scoring, ranking, or winner selection.
- No queue, runner, scheduler, or action-control behavior.

## Documentation targets

- `docs/OPERATOR_CONSOLE.md`
- `.specs/UI-ALPHA-OPERATOR-CONSOLE-DAILY-USE-WALKTHROUGH-001.md`
- `.specs/INDEX.md`

## Definition of done

- The Operator Console docs include a concise `Operator Console Daily-Use Walkthrough` section.
- The walkthrough builds on the existing First 5 Minutes section instead of duplicating it.
- The walkthrough is specific to the current protected `/dashboard/operator-console` cockpit after the First 5 Minutes lane.
- The walkthrough helps an operator identify reviewable, manual-only, and blocked behavior.
- The walkthrough tells the operator when a Local Receipt may be useful and when to skip it.
- The walkthrough makes confusion visible with a manual notes template that stays outside the console.
- The walkthrough does not add or imply code, UI, routing, write-path, or execution changes.

## Boundary checklist

- [x] Docs/process only.
- [x] No code changed.
- [x] No UI changed.
- [x] No new Operator Console card.
- [x] No new status key.
- [x] No new route or POST route.
- [x] No write path changed.
- [x] No execution behavior added.
- [x] Local Receipt Store remains the only controlled write surface.
- [x] Provider calls remain blocked inside the console.
- [x] ChatGPT calls remain blocked inside the console.
- [x] `/v1/solve` remains blocked inside the console.
- [x] Browser automation remains blocked inside the console.
- [x] Terminal command execution remains outside the console.
- [x] Paste storage and capture editing remain outside the console.
- [x] Raw prompt and raw output display remain blocked.
- [x] Scoring, ranking, and winner selection remain blocked.
- [x] Queue, runner, scheduler, and action controls remain out of scope.

## Non-claims

The walkthrough is operator-comprehension evidence only. It does not claim answer quality, route correctness, model superiority, provider readiness, billing accuracy, benchmark validity, production readiness, validation success, or execution safety beyond the currently documented console boundaries.
