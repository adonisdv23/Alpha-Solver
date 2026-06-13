# P2-001: D-1 through D-5 caveat source text

Status: resolved with in-repository source evidence. No caveat content is invented; everything below is quoted from committed files.

## Source locations

The caveat source text exists, identically, in two committed files:

- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/verification-annex/checker-caveats.md`
- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-verification-annex/checker-caveats.md`

## Source text (quoted verbatim)

> These caveats are recorded for Council visibility and are not treated as blockers for this documentation-only annex.
>
> - D-1: intentional missing-reference exemption terms such as deferred and does not exist are the loosest future false-negative channel; accepted as P3/deferrable because #490 is net safer and current live corpus is partitioned.
> - D-2: redundant checked-reference call can be simplified later; non-blocking.
> - D-3: minor style issue in tests; non-blocking.
> - D-4: lane checks-run.md remains self-attested prose; CI mitigates for #490.
> - D-5: AUDIT-005 authorization restated conditions instead of quoting verbatim; substantively compliant.
>
> Council should treat D-1 through D-5 as visible non-blocking caveats, not hidden blockers.

## Per-caveat boundedness review against the surfaced text

| Caveat | Subject | Recorded severity in source | Plausible P0/P1 on the surfaced text? |
|---|---|---|---|
| D-1 | Checker intentional-missing-reference exemption terms are a future false-negative channel | P3 / deferrable | No — a documentation-checker coverage limitation, with mitigation rationale recorded |
| D-2 | Redundant checked-reference call in the checker | non-blocking | No — cleanup item |
| D-3 | Minor style issue in tests | non-blocking | No |
| D-4 | Lane `checks-run.md` files are self-attested prose | mitigated by CI for #490 | No — a known self-attestation limitation, consistent with the VER-002 finding that declared process safety is not enforced safety |
| D-5 | AUDIT-005 authorization restated rather than quoted verbatim | substantively compliant | No |

Stop-condition check: none of the five surfaced caveats reveals a plausible P0/P1, so no escalation is triggered. The caveats remain visible. They are not marked resolved by this packet — this packet only supplies their source text so future reviewers can judge them directly. D-1 and D-4 should remain visible inputs to the release-gate review lane because they describe limits of the automated and self-attested checking that other evidence relies on.
