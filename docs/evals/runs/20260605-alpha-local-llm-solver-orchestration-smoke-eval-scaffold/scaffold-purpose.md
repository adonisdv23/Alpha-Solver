# Scaffold Purpose

## Purpose Statement

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

This scaffold exists to prepare the future smoke and evaluation packet for the local LLM solver orchestration integration. It is intended to be used only after a future implementation PR adds a local solver orchestration runner.

## In Scope

- Future runbook template for a non-production local orchestration runner smoke.
- Future local expert two-pass prompt set.
- Expected output field checklist.
- Future artifact capture and interpretation templates.
- Failure classification taxonomy.
- Redaction and evidence-boundary rules.
- Exactly one selected next lane.

## Out of Scope

- Implementing local solver orchestration.
- Executing a local LLM.
- Calling a hosted provider.
- Changing `/v1/solve`.
- Changing dashboard behavior.
- Importing smoke results.
- Claiming readiness, validation, superiority, benchmark performance, provider orchestration, or production suitability.
