# Stop Conditions

Stop and return for operator review if any of the following occur:

- PR #590 is not merged.
- Source-of-truth docs do not show the expected selected next state before this lane starts.
- An open PR edits the same source-of-truth docs or target packet path.
- Raw Alpha outputs or raw baseline outputs would need to be inspected.
- A provider, hosted model, local model, runtime endpoint, dashboard, public API, `/v1/solve`, external service, or Google Sheets mutation would be needed.
- A score change, rescoring, unblinding, source-map update, or release implementation would be needed.
- New dependencies would be needed.
- The packet cannot avoid broad value, readiness, benchmark, provider, local-model, security/privacy, production, public, partnership, Pi.dev integration, or Alpha-superiority claims.
- Changed Markdown fails narrative claim-safety lint and cannot be rewritten within the evidence boundary.
- Source-of-truth docs cannot agree on `OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001`.
