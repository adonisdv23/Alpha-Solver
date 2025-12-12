# Bugfix Spec: TITLE

## Goal
- State the expected behavior once the bug is fixed.

## Motivation
- Link the customer issue, regression, or incident driving the fix.

## Acceptance Criteria
- [ ] Reproduction steps no longer fail
- [ ] Logs / metrics confirm the fix

## Definition of Done
- [ ] Root cause documented in this spec
- [ ] Tests cover the regression path
- [ ] Release notes or runbooks updated if needed

## Code Targets
- Systems / files suspected to contain the defect
- Follow-ups needed after mitigation

## Test Plan
- `python -m pytest -q`
- Regression-specific manual / automated checks
