# Future Approval Checklist

## Use boundary

This checklist records the approval information a future operator would need. It is not approval to run anything today.

## Required approval fields

A future run must not start unless the operator can record:

- [ ] Approver name or role.
- [ ] Approval timestamp.
- [ ] Approved branch, commit SHA, and artifact directory.
- [ ] Approved task statement.
- [ ] Explicit non-goals.
- [ ] Approved provider/runtime mode.
- [ ] Approved fallback mode, including whether fallbacks are disabled.
- [ ] Approved credential and secret handling.
- [ ] Approved budget/spend limits, if any provider or hosted service is in scope.
- [ ] Approved file write scope.
- [ ] Approved stop conditions.
- [ ] Approved archive/closeout destination.

## Approval mismatch rule

If the live task, branch, provider, fallback, credentials, budget, file scope, or artifact path differs from the approval record, the operator must stop and obtain new approval before proceeding.
