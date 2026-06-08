# MVP Allowed Scope

## Earliest allowed planning scope

If the selected Level 9 planning lane is accepted, it may plan only a narrow operator-only Self Operator MVP with these defaults:

- Local-only execution.
- Operator-supervised starts, stops, approvals, and reviews.
- No provider calls.
- No hosted model calls.
- No external API calls.
- No browser control.
- No deployment.
- No billing or cost-incurring behavior.
- No autonomous merge.
- No evidence promotion.

## Planning topics allowed

The selected planning lane may define future implementation requirements for:

- local task/job records;
- local lifecycle state transitions;
- local artifact persistence;
- explicit human approval checkpoints;
- stop-before-start preflights;
- deterministic local checks;
- acceptance tests required before MVP readiness can be claimed;
- operator runbook handoffs;
- future code-change gates.

## Not yet authorized

Even inside the selected planning lane, the project may not implement Self Operator, run Self Operator, call providers, run models, expose `/v1/solve`, expose dashboards, deploy, bill, autonomously merge, control browsers, or promote evidence.
