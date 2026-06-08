# Future Monitoring Checklist

## Use boundary

This checklist describes future monitoring expectations only. It does not assert that a monitorable Self Operator process exists today.

## During-run monitoring

While a future Self Operator run is active, the operator must monitor:

- [ ] Run status and heartbeat.
- [ ] Current task phase and next planned action.
- [ ] Files created, modified, deleted, or staged.
- [ ] Branch cleanliness and unexpected worktree changes.
- [ ] Provider/runtime selection and fallback state.
- [ ] Credential exposure risk in logs, artifacts, stdout, stderr, and diffs.
- [ ] Budget/spend counters where applicable.
- [ ] Network, deploy, route, or external side-effect attempts.
- [ ] Test/check execution and failures.
- [ ] Artifact completeness and redaction status.
- [ ] Any deviation from approved task, scope, or stop conditions.

## Immediate monitor stops

Stop the future run if monitoring shows:

- missing or contradictory evidence;
- missing or mismatched approval;
- unclear task evolution;
- provider or fallback ambiguity;
- possible credential leak;
- branch pollution or unexpected destructive file action;
- uncontrolled external side effect;
- artifact capture failure;
- operator uncertainty about safety or scope.
