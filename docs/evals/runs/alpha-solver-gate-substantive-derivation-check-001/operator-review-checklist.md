# Operator Review Checklist

Use this checklist before authorizing any later implementation or fixture execution lane.

- Confirm the packet is docs-only and review-only.
- Confirm source-of-truth docs list `OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001`.
- Confirm no raw Alpha outputs or raw baseline outputs were inspected.
- Confirm no scores were changed.
- Confirm criteria distinguish exact echo, near echo, paraphrase-only response, substantive derivation, acceptable source use, unsupported copying, and non-answer safe-out.
- Confirm fixture labels are frozen before any future deterministic checker run.
- Confirm safe-out markers cannot convert copied prompt text into a passing result.
- Confirm the packet makes no broad value, readiness, benchmark, provider, local-model, public API, production, security/privacy, partnership, Pi.dev integration, or Alpha-superiority claim.
- Confirm any future implementation lane is separately authorized and narrowly scoped.
