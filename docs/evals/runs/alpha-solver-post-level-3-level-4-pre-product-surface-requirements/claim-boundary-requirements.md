# Claim-Boundary Requirements

## Required claim matrix

Every later lane must maintain a claim matrix with these columns:

- proposed claim;
- allowed, blocked, or deferred status;
- required evidence category;
- required artifact path;
- review status;
- freshness requirement;
- contradiction handling rule;
- fallback or rollback action.

## Boundary rules

- Level 2 evidence may be described only as local operator usability evidence.
- Level 3 evidence may be described only as artifact-complete, non-promotional local orchestration evidence.
- Design packets may describe requirements and plans only.
- Execution packets may create execution evidence only when separately authorized.
- No packet may convert local orchestration artifacts into production, MVP, benchmark, model-quality, provider, dashboard, API, billing, or superiority evidence without a later lane that explicitly authorizes and bounds that evidence.

## Documentation requirements

Every downstream packet must include claim-boundary text near any mention of readiness, quality, benchmark, provider, billing, dashboard, `/v1/solve`, MVP, or production terminology. The packet must prefer explicit blocked-claim wording over ambiguous promotional wording.
