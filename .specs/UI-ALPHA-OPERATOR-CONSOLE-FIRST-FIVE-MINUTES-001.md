# UI-ALPHA-OPERATOR-CONSOLE-FIRST-FIVE-MINUTES-001 · Operator Console First 5 Minutes Guide

Lane id: `AOC-DOCS-FIRST-FIVE-MINUTES-001`

## Goal

Add a short plain-English onboarding section to `docs/OPERATOR_CONSOLE.md` that tells a daily operator what to look at first in the protected Operator Console and how to interpret the current local-first surfaces.

This is a docs/onboarding lane only. It makes the current cockpit easier to understand without making the console more capable.

## Scope

- Add an `Operator Console First 5 Minutes` section to the Operator Console documentation.
- Explain the one-sentence purpose of the console.
- Add a short first five-minute checklist.
- Explain the current surfaces card by card:
  - Local Artifact Status
  - Freshness and Sequence Coherence
  - Provider, Model, and Cost Gate
  - Dry-Run Preview
  - Local Receipt Store
  - ChatGPT Copy/Paste Capture
  - Manual Next Step Guide
  - Route/Trace placeholders
- State what must be done manually outside the console.
- State when to create a local receipt.
- State how to interpret Dry-Run Preview as display-only metadata.
- State what the console does not prove.
- Add a concise do-not-expect list for blocked behavior.

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
- `.specs/INDEX.md`

## Definition of done

- The documentation includes the required `Operator Console First 5 Minutes` section.
- The guide is specific to the current protected `/dashboard/operator-console` surface after the Manual Next Step Guide lane.
- The guide uses plain-English operator language.
- The guide keeps terminal commands, capture edits, ChatGPT copy/paste, and raw evidence review outside the console.
- The guide identifies the Local Receipt Store as the only controlled local write surface.
- The guide does not add or imply code, UI, routing, write-path, or execution changes.

## Boundary checklist

- [x] Docs-only.
- [x] No code changed.
- [x] No UI changed.
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

## Non-claims

The guide does not claim readiness, validation success, benchmark validity, production readiness, scoring, ranking, winner selection, model superiority, provider readiness, billing accuracy, or answer quality.
