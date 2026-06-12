# Fable audit findings reviewed

source_type: same_thread_fable_chat_report
source_title: Alpha Solver — Final Independent Read-Only Audit Report
repo_artifact_found: no
operator_context_available: yes
findings_used:
  F-1
  F-2
  F-6
audit_boundary:
  external chat audit source, not a committed repo artifact

## Repo artifact search result

The read-only repo search for a committed final independent read-only audit report or Council-prep audit artifact did not find a committed artifact containing F-1, F-2, F-6, and AUDIT-005 together. Existing committed triage files record `AUDIT-005`, but not the final independent read-only Fable findings F-1, F-2, and F-6 as a completed audit report.

## Findings used

- F-1 High/P1 was used as the future checker-scope boundary: the final independent read-only Fable audit reported that the forbidden-claim checker and doc-path checker do not scan `alpha-solver-post-*` packet directories. This lane records that F-1 remains open for a future checker-scope extension lane and does not modify checker scripts or tests.
- F-2 Medium/P2 was used as the Council bundle routing and wording basis: the final independent read-only Fable audit reported that the Council audit evidence bundle has ambiguous blocker/fallback routing and unclear `clean after required checks` wording. This lane repairs only the derivative Council bundle routing and wording.
- F-6 Low/P3 was used as the AUDIT-005 decision basis: the final independent read-only Fable audit reported that `AUDIT-005` remained open and gated combined tooling/docs lanes, including the future F-1 checker-scope extension lane.
- AUDIT-005 was reviewed as the open operator-decision item requiring exact approval text before combined tooling/docs or multi-blocker work proceeds.

## Boundary

This file records the findings reviewed for this lane. It does not turn the external chat audit source into raw repo execution evidence, does not run Council, and does not resolve F-1.
