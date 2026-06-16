# Stop Conditions

A future unblinding/source-identity review and final interpretation pass must stop if any condition below is true.

## Authorization defects

- No explicit future operator authorization exists.
- The future pass tries to treat this packet as the unblinding authorization itself.
- The future pass lacks a distinct lane id.

## Score-lock defects

- The locked score-output file is missing.
- The future pass cannot verify the locked score-output file.
- Any score, note, contested-score flag, scorer field, scoring method, timestamp, or score-lock confirmation would need to change.

## Source-identity defects

- The identity map is missing, incomplete, ambiguous, or not approved for use.
- The future pass would need to infer identities from content or style.
- A source identity cannot be attached to a locked score row without ambiguity.

## Scope defects

- The future pass would need provider calls, local model runs, raw output inspection beyond a separately authorized discrepancy review, runtime endpoint exposure, dashboard/public API exposure, `/v1/solve` exposure, Google Sheets mutation, dependency additions, or release-lane implementation.
- The future pass would need to make value, readiness, benchmark, provider, local-model, production, public, security/privacy, partnership, Pi.dev integration, or Alpha-superiority claims.
