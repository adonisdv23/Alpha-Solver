# Evidence Boundaries

Post-Level-3 packets must keep evidence claims bounded to the artifacts they actually create or review.

## Current boundary to preserve

Future packets should preserve these constraints unless a later approved lane produces new bounded evidence:

- Level 2 remains local operator usability evidence only.
- Level 3 remains artifact-complete, non-promotional local orchestration evidence only.
- Release-readiness ladder work defines future gates; it does not complete those gates.
- Docs-only authoring packets do not prove runtime, provider, product, dashboard, billing, benchmark, or MVP readiness.

## Avoid promoting Level 2 and Level 3 evidence

Do not use Level 2 or Level 3 local-only evidence as proof of product readiness, model quality, hosted-provider readiness, provider fallback readiness, dashboard readiness, `/v1/solve` readiness, benchmark performance, billing readiness, Alpha superiority, or MVP readiness.

Safe wording:

> Level 3 is closed as artifact-complete, non-promotional local orchestration evidence only.

Unsafe wording:

> Level 3 proves that Alpha Solver is ready for users, hosted providers, dashboards, and benchmarks.

## Preserve blocked claims

A packet may list blocked claims to make boundaries explicit. Blocked claims should remain blocked until a later approved packet defines and satisfies the necessary evidence requirements.

Safe wording:

> This packet does not establish production readiness, MVP readiness, benchmark evidence, provider-orchestration evidence, dashboard readiness, `/v1/solve` readiness, or billing readiness.

Unsafe wording:

> Because the docs are complete, readiness is established.

## Checks-run files are not authoritative evidence

`checks-run.md` records commands and outputs used to validate packet consistency. It should not be the only place where selected-next state, fallback state, final decisions, or evidence boundaries appear.

Safe wording:

> The selected-next action is recorded in `selected-next-action.md`; `checks-run.md` only records that checks were run.

Unsafe wording:

> The selected-next action exists because it appears in the `rg` command output in `checks-run.md`.

## Evidence boundary for this guide

This guide is docs-only authoring guidance. It does not start Level 4, run models, run Ollama, rerun validation, call hosted providers, expose `/v1/solve`, expose dashboard routes, add fallback, run benchmarks, perform billing work, or promote evidence.
