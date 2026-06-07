# Candidate Task Families

These families are candidates for future quality evaluation design discussion only. They are not a frozen task set and do not authorize execution, scoring, benchmarking, or quality claims.

## Prompt-contract preservation

Tasks may examine whether responses preserve explicit user instructions, scope limits, output-format requirements, and non-action boundaries without adding unsupported work.

## Evidence-boundary correction

Tasks may examine whether responses identify overclaims, unsupported evidence promotion, or claims that exceed accepted Level 2, Level 3, Level 4, or later boundaries.

## Lane continuity and selected-next state

Tasks may examine whether documentation preserves exactly one selected-next action or lane where required, avoids contradictory no-further-lanes state, and records blocker fallback state clearly.

## Artifact review

Tasks may examine whether packet artifacts are complete, internally consistent, source-bounded, and limited to allowed paths.

## Claim-boundary review

Tasks may examine whether responses avoid claims about quality, product readiness, provider readiness, dashboard readiness, `/v1/solve` readiness, billing readiness, benchmark evidence, production readiness, or Alpha superiority unless explicitly supported by authorized evidence.

## Local operator guidance

Tasks may examine whether operator-facing documentation is precise, non-promotional, reproducible, and clear about prerequisites, local-only boundaries, and non-execution limits.

## Failure-mode triage

Tasks may examine whether observed failures are classified without overstating root cause, introducing unapproved fallback, or changing behavior outside an authorized lane.

## Source-evidence interpretation

Tasks may examine whether a response distinguishes source artifacts, imported evidence, summaries, check outputs, and implementation contracts without treating provenance artifacts or backlog ledgers as implementation authority.

## Docs-only packet review

Tasks may examine whether docs-only packets stay within approved file paths, avoid runtime changes, include required non-actions, and record checks without promoting documentation to execution evidence.

## Future product-surface safety review

Tasks may examine future product-surface proposals for safety boundaries around user-facing exposure, API routes, dashboards, provider orchestration, fallback, billing, and readiness claims before any product-surface work starts.
