# Evidence Boundary

This packet may prove only what was actually run locally and offline.

## What this packet proves

- The Self Operator code under `alpha/self_operator/` **executes locally and deterministically**: its
  full test suite runs green (213/213), and its release-gate checker CLI runs to completion (exit 0,
  11/11 gates pass) against live in-repo evidence.
- This execution required **no provider, no model, no token, no hosted service, and no external API**.
- The full test suite, run with provider env vars unset, passes 1211/1216; consistent with the PR #496
  recorded full-suite behavior, it still reports the same two unrelated environment-level (commit-signing)
  failures, plus 3 expected skips.

## What this packet does NOT prove

- It does not prove provider behavior, OpenAI behavior, or any hosted behavior.
- It does not prove runtime readiness, public MVP readiness, or production readiness.
- It does not complete or substitute for the DEF-002 product security/privacy review.
- It does not validate benchmark performance or benchmark superiority.
- It does not prove broad-user readiness, autonomous readiness, `/v1/solve` readiness, or dashboard
  readiness.
- A passing release-gate inspection is a **static file-presence** check; it is explicitly **not** an
  MVP/release readiness claim (the checker says so itself).

## DEF-001 status: `DEF-001_PARTIALLY_RETIRED`

This lane **partially** retires DEF-001 rather than fully retiring it.

Why partial (genuine progress):
- DEF-001's own definition names "logs, test-run records, or runtime artifacts demonstrating behavior" as
  the missing evidence. This lane produces real **test-run records** and a real **CLI run artifact** for
  the Self Operator candidate, captured under the local/offline boundary.

Why not full:
- The complete intended flow is **operator-supervised end-to-end on a representative candidate task**
  (preflight → execution-gate → dry-run artifact → recorded operator approval/decision → result import →
  acceptance interpretation), with operator decisions recorded. This lane exercised those stages at the
  component/test level and ran one operator-invokable checker, but did not perform a single end-to-end
  operator-supervised run on a representative candidate task with recorded operator decisions.
- Full retirement inherently requires operator participation (the operator supervises and decides), which
  is out of scope for this automated lane.

## What remains blocked

- **DEF-001 (full):** an operator-supervised end-to-end run on a representative candidate task with
  recorded operator decisions (the selected next lane).
- **DEF-002:** product-level security/privacy review (threat model, secret scan, dependency vulnerability
  analysis, privacy assessment) — required before any exposure beyond operator-supervised local use.
- **DEF-003:** prior targeted Fable delta audit full text (operator-held); may be cited only as
  "reported no P0/P1 blockers".
- All provider/token/hosted/runtime/benchmark work, and any public/production/`/v1/solve`/dashboard/
  autonomous exposure.
