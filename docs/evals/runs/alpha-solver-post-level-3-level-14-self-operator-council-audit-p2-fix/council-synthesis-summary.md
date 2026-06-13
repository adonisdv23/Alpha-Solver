# Council run and synthesis summary

This is a bounded summary for repository traceability. The controlling documents — the cleaned raw capture file and `ALPHA-SOLVER-COUNCIL-SYNTHESIS-REPORT-001` — are operator-held outside this repository (see `deferral-register.md` DEF-004).

## Council run outcome

- Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-MANUAL-RUN-001`.
- Capture result: 16 usable raw audit responses plus 1 documented failed platform slot.
- Failed platform slot: slot 05, Venice - Auto, Security / Privacy Auditor lens, status `PLATFORM_FAILED_NO_USABLE_OUTPUT`, with a formal operator capture note. No response was reconstructed or fabricated. The slot is not counted as substantive Council evidence.
- Lens-coverage limitation: the Security / Privacy lens was assigned to two seats and one failed, so that lens rests on a single substantive seat in this run.

## Findings profile reported by the 16 usable seats

- P0 hard blockers reported: 0 across all 16 seats.
- P1 major blockers reported: 0 across all 16 seats.
- Recommendation tally: 8 seats selected `COUNCIL-AUDIT-P2-FIX-001`, 7 seats selected `RELEASE-GATE-APPLY-001` (each with preconditions substantially matching the P2 set), 1 seat selected `STOP-INCONCLUSIVE`.
- All 16 seats marked caveats D-1 through D-5 as visible but under-explained, because the Council evidence packet omitted their source text.

## Synthesis decision

The synthesis selected a P2 hardening lane with this required item set:

- P2-001: supply D-1 through D-5 source text or record per-caveat deferrals.
- P2-002: supply #492 / F-1 correction primary evidence or record a deferral.
- P2-003: define release-gate acceptance criteria, including Self Operator package scope.
- P2-004: record an explicit deferral for missing Self Operator execution evidence.
- P2-005: record an explicit deferral for the missing product-level security/privacy review.
- VER-001: open the lane with fresh read-only repo-state verification.
- VER-002: check for no-go-list enforcement artifacts before deciding on hardening.
- DOC-001, DOC-002, DOC-003: wording, consensus-interpretation, and capture-integrity process corrections.

## Interpretation limits

Council agreement in this run is agreement over one shared evidence packet. It is replication of that packet's assertions, not independent corroboration of repository, runtime, or product state. The zero-P0/P1 result certifies that no seat found a blocker in the provided evidence; it does not certify the project state. The prior targeted Fable delta audit reported no P0/P1 blockers; that is a summarized model/auditor judgment and is cited only as such.
