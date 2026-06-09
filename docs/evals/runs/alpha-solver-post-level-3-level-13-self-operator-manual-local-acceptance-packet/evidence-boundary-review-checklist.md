# Evidence-Boundary Review Checklist

The operator must block or stop on any of the following:

- [ ] Provider calls.
- [ ] Hosted model calls.
- [ ] Local model calls unless a later lane explicitly allows them.
- [ ] External API calls.
- [ ] Credentials.
- [ ] Secret access.
- [ ] Browser automation.
- [ ] Deployment.
- [ ] Billing.
- [ ] `/v1/solve` exposure.
- [ ] Dashboard exposure.
- [ ] Product CLI behavior changes.
- [ ] Fallback or hosted fallback behavior.
- [ ] Source-artifact mutation.
- [ ] Evidence promotion.
- [ ] Autonomous approval.
- [ ] Autonomous merge.
- [ ] Missing operator confirmation.
