# Readiness Ladder Overview

## Design principle

The release-readiness ladder is a sequence of gates, not a sequence of claims. Each future level must define or gather bounded evidence before later work can proceed.

## Ladder sequence

1. Level 4, `PRE_PRODUCT_SURFACE_REQUIREMENTS`, defines requirements and safety gates before product surface planning.
2. Level 5, `QUALITY_EVALUATION_DESIGN`, defines quality evaluation methodology before benchmarks or quality runs.
3. Level 6, `PRODUCT_SURFACE_DESIGN`, defines `/v1/solve` and dashboard prerequisites before exposing product surfaces.
4. Level 7, `PROVIDER_ORCHESTRATION_DESIGN`, defines hosted-provider, fallback, credential, privacy, billing, and fail-closed requirements before provider orchestration implementation.
5. Level 8, `MVP_READINESS_REVIEW`, reviews whether prior gates produce enough bounded evidence to consider MVP readiness without claiming it in this packet.

## Why Level 4 is first

Level 4 is selected first because Alpha Solver needs requirements, safety gates, claim boundaries, and evidence requirements before any downstream product, quality, provider, billing, dashboard, `/v1/solve`, or MVP readiness lane can be safely scoped. Starting quality evaluation, product surface design, or provider orchestration first would risk treating Level 2 and Level 3 local-only evidence as broader readiness evidence.

## Deferred work

- Quality evaluation is deferred until Level 4 defines evidence requirements and claim boundaries.
- Product surfaces are deferred until Levels 4 and 5 define requirements, evidence limits, and quality methodology.
- Provider orchestration is deferred until Levels 4 through 6 define safety, privacy, observability, and surface requirements.
- MVP readiness is deferred until Levels 4 through 7 have been completed by future packets and reviewed with bounded evidence.
