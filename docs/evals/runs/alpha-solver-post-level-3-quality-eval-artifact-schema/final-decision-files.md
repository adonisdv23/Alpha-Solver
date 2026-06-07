# Final Decision Files Schema

## Purpose

Final decision files record what a future eval artifact packet concludes. Checks-run files record commands and checks. The two must not be conflated.

## What belongs in final decision files

Future `final-decision.md` files should contain:

- Final decision state: accepted, rejected, blocked, inconclusive, deferred, or superseded.
- Scope of the decision and adopted schema reference.
- Raw outputs, reviewer notes, scoring records, invalid markers, and redaction logs considered.
- Excluded artifacts and the reason for exclusion.
- Claim-boundary language for the decision.
- Level 5 authorization or limitation statement.
- Required follow-up or explicit no-further-action marker.
- Signoff roles and decision timestamp.

## What belongs in checks-run files

Future `checks-run.md` files should contain:

- Commands run while assembling or validating the artifact packet.
- Pass, fail, or warning status for each command.
- Environment limitations for warnings.
- Paths inspected by static checks.
- Confirmation that forbidden actions were not run.

## Separation rule

A passing check does not by itself create a final quality decision. A final decision may cite checks-run status, but the decision must be based on the reviewed artifact inventory, raw-output preservation state, scoring records, invalid-result markers, redaction state, and Level 5 authorization.

## Required final decision claim-boundary language

Future final decision files must include:

"This final decision applies only to the artifacts identified in this packet and only within the Level 5 authorization boundary. It does not create eval evidence beyond the preserved raw outputs, reviewed scoring records, and explicitly accepted decision scope."
