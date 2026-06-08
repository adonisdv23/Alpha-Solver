# Stop conditions

Stop and do not continue if:

1. Any change would be outside this acceptance/release bridge packet directory.
2. Any source code, tests, fixtures, CI, scripts, runtime files, provider files, API files, dashboard files, CLI files, credential files, deployment files, billing files, Google Sheets files, source artifacts, or evidence payloads would need to change.
3. A lane would need to claim acceptance was run.
4. A lane would need to claim MVP readiness.
5. A lane would need to promote evidence.
6. The local-only acceptance evidence boundary cannot be preserved.
7. The operator-confirmation hard stop cannot be found in the current prompt pack.
8. Explicit operator confirmation is missing.
