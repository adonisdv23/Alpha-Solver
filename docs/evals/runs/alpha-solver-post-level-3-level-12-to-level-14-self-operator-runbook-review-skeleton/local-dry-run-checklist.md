# Local Dry-run Checklist

Use this checklist only after implementation lanes are merged and GS done.

- [ ] Explicit operator confirmation present.
- [ ] Hard-stop rule present: stop if explicit operator confirmation is missing.
- [ ] Run is local-only.
- [ ] Run is operator-supervised.
- [ ] No provider calls.
- [ ] No hosted model calls.
- [ ] No external APIs.
- [ ] No browser automation.
- [ ] No deployment.
- [ ] No billing.
- [ ] No credentials used or requested.
- [ ] No Google Sheets updates.
- [ ] No source-artifact mutation.
- [ ] Allowed local output directory confirmed.
- [ ] Redacted artifact path confirmed.
- [ ] Stop-state behavior confirmed.
- [ ] Evidence boundary preserved.
