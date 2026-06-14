# Failure Analysis

Failure class: `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`.

The lane was selected by current repo docs and PR #512 records the redacted project/billing boundary confirmation, but the execution prompt for this run did not supply all required live-call parameters:

- explicit model;
- explicit project boundary for this run;
- explicit cost cap;
- explicit token cap;
- explicit max run count;
- exact synthetic prompt fixture payload.

Resolution: obtain a fresh operator authorization packet containing every required field, then retry only the same tiny synthetic smoke boundary. Do not run broad evals or value tasks as part of that retry.
