# Allowed use scope

What the operator may do next, after this prep packet is accepted. Everything
here is operator-supervised, local-only, and bounded by the canonical runbook
and `operator-use-contract.md`.

## The operator may

1. Review this prep packet, the closeout packet, the repair packet, and the
   canonical runbook, read-only.
2. Charter the first supervised-use lane
   (`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-PACKET-001`)
   with its own lane ID, fresh run ID, allowed file list, and packet
   directory.
3. In that chartered lane only, and only after completing
   `first-use-checklist.md` and the confirmation in
   `operator-confirmation-requirements.md`, exercise the local-only
   gate-and-record pipeline that the accepted evidence chain already
   exercised: preflight classification, approval validation, the corrected
   execution gate, and the local dry-run wrapper
   (`alpha.self_operator.dry_run.run_local_dry_run_wrapper`) with an explicit
   output root. The wrapper classifies proposed command text; it does not
   execute proposed commands.
4. Persist and review the wrapper's redacted local artifacts
   (`dry-run-result.json`, `execution-gate-result.json`, and
   `stop-state.json` when stopped) below the output root, and import only
   redacted copies into that lane's packet through lane review.
5. Run the deterministic local documentation checks read-only at any time:
   `python scripts/check_self_operator_release_gate.py --repo-root .` and
   `python scripts/check_local_llm_packet_consistency.py`.
6. Record defects with severity and disposition in the owning lane's packet,
   and route to the blocker-fix lane per `stop-state-response-plan.md` when a
   defect or stop condition appears.

## Bounds on this scope

- Nothing in this scope authorizes any item in `forbidden-actions.md`.
- Nothing in this scope may be performed outside a chartered lane with its
  own approval record and run ID.
- This prep lane itself performed none of the above use steps; it only
  prepared them.
