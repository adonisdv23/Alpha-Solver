# Evidence Boundary Review Checklist

The future acceptance/release reviewer must block any scope involving:

- [ ] Provider calls.
- [ ] Hosted model calls.
- [ ] Local model calls unless explicitly allowed by a later lane.
- [ ] External API calls.
- [ ] Credentials.
- [ ] Secret access.
- [ ] Browser automation.
- [ ] Deployment.
- [ ] Billing.
- [ ] `/v1/solve` exposure.
- [ ] Dashboard exposure.
- [ ] Product CLI behavior changes.
- [ ] Fallback.
- [ ] Hosted fallback.
- [ ] Source-artifact mutation.
- [ ] Evidence promotion.
- [ ] Autonomous merge.
- [ ] Autonomous approval.
- [ ] Missing operator confirmation.

This checklist preserves a local-only, operator-supervised evidence boundary.
