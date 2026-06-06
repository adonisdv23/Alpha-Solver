# Implementation Boundary

## Docs-only current lane

This lane creates a canonical spec and supporting docs only. It must not change source code, test code, runtime behavior, provider behavior, `/v1/solve`, dashboard preview, Google Sheets, smoke artifacts, or output evidence.

## Future implementation lane boundary

The future implementation lane may add the non-production runner and focused tests needed for `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`.

It must not expose local LLM orchestration through production `/v1/solve` or dashboard preview, must not add hosted fallback, and must not modify evidence-model semantics.

## Built code versus approved surfaces

Existing built code surfaces are not automatically approved runtime integration surfaces. Reference entrypoints, provider routes, preview routes, deterministic reasoning utilities, local runtime seams, and legacy files require explicit approval before being used as local LLM orchestration surfaces.

`alpha_solver_v225_p2_experts.py` is not active unless separately approved as non-stub.
