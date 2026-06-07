# Pre-Product-Surface Gates

No product-surface, quality, provider, dashboard, API, billing, or MVP readiness lane may proceed unless these gates are satisfied.

## Gate 1: accepted evidence boundary

The lane must import the accepted Level 2 and Level 3 decisions without expanding them. The Level 3 accepted state remains `LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE` with `NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED`.

## Gate 2: source-evidence review

The lane must list reviewed source evidence and identify which files are preserved artifacts, which files are design documents, and which files are current operational guardrails.

## Gate 3: blocked-claim inventory

The lane must include blocked claims and non-actions before any design or execution work. Blocked claims must include production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, and evidence-model promotion unless a later authorized lane produces bounded evidence for that exact claim.

## Gate 4: evidence requirements

The lane must define the evidence categories it needs, the evidence categories it excludes, the pass/fail criteria it will use, and the artifacts it will preserve.

## Gate 5: operator controls and observability

The lane must define required controls, logs, traceability, stop conditions, and review artifacts before any later runtime, route, provider, dashboard, or billing work can be proposed.

## Gate 6: fallback and rollback

The lane must define a blocker fallback lane and must stop instead of continuing when evidence is missing, stale, contradictory, overbroad, or unsafe.
