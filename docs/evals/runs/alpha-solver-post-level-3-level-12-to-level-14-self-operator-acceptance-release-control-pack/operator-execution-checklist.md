# Operator Execution Checklist

Before future manual local acceptance execution, confirm:

- [ ] Explicit operator confirmation is present; stop if explicit operator confirmation is missing.
- [ ] Correct branch and source commit are checked out.
- [ ] Working tree is clean.
- [ ] Command scope is local-only and operator-supervised.
- [ ] Temporary output root is selected and outside source artifacts.
- [ ] No source artifact mutation will occur.
- [ ] No network/provider/API/browser/deploy/billing/credential/Google Sheets access is required or allowed.
- [ ] Redaction review process is defined before artifact sharing.
- [ ] Stop-state behavior is documented and observable.
- [ ] Artifact persistence path is local-only and known.
- [ ] Abort conditions are documented before execution.
