# Future Artifact Review

## Use boundary

This review checklist applies only after a future authorized Self Operator run exists. It does not create behavior evidence for Self Operator today.

## Artifact review checklist

The operator must verify that future run artifacts include:

- [ ] Run identifier, branch, commit SHA, operator, approver, and timestamps.
- [ ] Exact start command or entrypoint provenance.
- [ ] Approved task statement and non-goals.
- [ ] Preflight and approval records.
- [ ] Provider/runtime/fallback configuration summary without secrets.
- [ ] Stop conditions active during the run.
- [ ] Log, stdout, stderr, or transcript captures where approved.
- [ ] File diff summary and changed-file list.
- [ ] Test/check commands and outcomes.
- [ ] Redaction review result.
- [ ] Stop/recovery record if the run stopped early.
- [ ] Closeout decision and selected-next or no-further-action state.

## Artifact rejection criteria

Artifacts must not be accepted if they contain secrets, omit provenance, omit approval, hide provider/fallback behavior, blur task scope, include unrelated branch changes, or claim readiness/safety/performance beyond the approved evidence boundary.
