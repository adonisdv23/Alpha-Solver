# SOLVE-SANITIZER-FALSE-POSITIVE-001 · Narrow Import-Substring Sanitizer Fix

## Goal

Fix the `/v1/solve` input sanitizer false positive that rejects benign natural-language words containing the substring `import`, including the approved A3-1 prompt `HHE-009` beginning with `IMPORTANT`.

## Root cause

The current sanitizer treats any lowercase query containing the substring `import` as a disallowed pattern. This blocks ordinary words such as `IMPORTANT`, `important`, `importance`, and `importantly` before provider or local solver execution.

## Scope

- Replace naive substring matching with token-aware import syntax detection.
- Allow benign natural-language substrings containing `import`.
- Continue blocking risky Python import/code patterns, including:
  - `import os`
  - `import subprocess`
  - `from os import system`
  - `__import__("os")`
- Add focused sanitizer and `/v1/solve` input-validation regression tests for the A3-1 prompt subset.

## Non-goals

- No A3-1 capture execution.
- No provider calls.
- No eval artifact population, scoring, or unblinding.
- No provider routing, expert-pass, dashboard rendering, dashboard auth, tool routing, effort toggle, or quota behavior changes.
- No claims of MVP validation, Alpha Solver superiority, answer-quality superiority, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.

## Acceptance criteria

- The exact `HHE-009` prompt passes `/v1/solve` input validation.
- Benign phrases containing `important`, `importance`, `IMPORTANT`, and `importantly` pass sanitization.
- Actual import syntax remains rejected.
- Existing secret/cookie/session/auth protections and no-secret tests remain unchanged.
