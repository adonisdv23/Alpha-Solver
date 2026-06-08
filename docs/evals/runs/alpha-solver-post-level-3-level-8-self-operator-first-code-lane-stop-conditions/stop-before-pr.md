# Stop before PR

A future first code lane must stop before opening a PR if any of these checks fails:

- Level 8 is accepted.
- A concrete implementation lane is selected.
- The branch is current-main-based.
- The committed files are within the selected lane's allowed scope.
- The committed files do not introduce provider call risk.
- The committed files do not introduce credential risk.
- The committed files do not introduce browser automation.
- The committed files do not introduce deployment.
- The committed files do not introduce billing.
- The committed files do not introduce external API behavior.
- The committed files do not expose or modify `/v1/solve` or dashboard behavior.
- The committed files do not promote evidence.
- The committed files do not modify source artifacts.

If any check fails, the future operator must not open a PR and must use the blocker fallback lane if a corrective docs-only stop-condition fix is needed.
