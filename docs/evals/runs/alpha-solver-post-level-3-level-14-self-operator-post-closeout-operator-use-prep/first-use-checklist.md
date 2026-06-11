# First-use checklist

The checklist a future operator must complete before a first supervised use
of the Self Operator path after closeout. This checklist defines the steps
only. Nothing on this checklist was executed by this prep lane, and
completing it is itself a documentation activity until the chartered
supervised-use lane authorizes the run.

## Preconditions on `main`

- [ ] Closeout packet present with
      `final_status: eligible_for_operator_supervised_review`.
- [ ] Post-closeout release-gate report present with
      `release_closeout_review_complete: pass` and final status
      `eligible_for_release_closeout_review`.
- [ ] This prep packet merged on `main`.
- [ ] A fresh read-only run of
      `python scripts/check_self_operator_release_gate.py --repo-root .`
      exits 0 on the checkout that will be used.

## Lane and approval setup

- [ ] First supervised-use lane chartered
      (`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-PACKET-001`)
      with an allowed file list and its own packet directory.
- [ ] Fresh `run_id` assigned for this run only.
- [ ] Approval record drafted with every required field from
      `operator-confirmation-requirements.md`, including the verbatim guard
      text and `redaction_status: redacted`.
- [ ] Proposed task carries explicit `lane_id`, `metadata.run_id`, and
      metadata scope identity so every identity dimension is comparable.

## Environment and output setup

- [ ] Local output root chosen outside the repository tree per
      `artifact-output-root-plan.md`; confirmed empty and writable.
- [ ] No credentials or secrets present in any input the run will read.
- [ ] Redaction expectations from `redaction-and-secrets.md` reviewed; the
      pre-import redaction review is planned.

## Boundary review

- [ ] `forbidden-actions.md` reviewed; the approval text authorizes none of
      it.
- [ ] `evidence-preservation-rules.md` reviewed; all sources will be
      consumed read-only.
- [ ] `non-execution-proof-requirements.md` reviewed; the proof artifacts
      this run must preserve are identified before the run.
- [ ] `stop-state-response-plan.md` reviewed; the operator knows every stop
      condition and the blocker-fix routing before starting.
- [ ] The operator can state the exact allowed claim from
      `operator-use-contract.md` and confirms no other claim will be made.

## Final gate before the run

- [ ] Explicit operator confirmation recorded for this lane and this run.
- [ ] If any box above is unchecked, or anything is unclear: do not run.
      Unclear means stop; route per `stop-state-response-plan.md`.
