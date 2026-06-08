# Run Status Copy

## Task intake status

Required copy:

> Intake received. Review task scope, requested outputs, evidence boundary, artifact destination, and provider-call boundary before approval.

## Preflight result status

Pass copy:

> Preflight passed. The task can be presented for operator approval within the documented boundary.

Warning copy:

> Preflight warning. Review the warning before approval; the task may continue only if the warning is acceptable within scope.

Blocked copy:

> Preflight blocked. The task cannot proceed until the listed blocker is resolved.

## Running status

Required copy:

> Running within approved scope. Monitor current step, stop option, and artifact location.

The status view must show:

- Current state.
- Current step or phase.
- Last update time or event sequence.
- Stop option.
- Artifact path or pending artifact reservation.
- Warning count, if any.

## Stop state status

Stop requested copy:

> Stop requested. The Self Operator is attempting to halt within the approved boundary.

Stopped copy:

> Stopped. Review partial artifacts and logs before re-running or closing the task.

Stop failed copy:

> Stop failed or incomplete. Treat the run as blocked and review logs before taking further action.

## Completed status

Required copy:

> Completed. Review generated artifacts, warnings, non-actions, and evidence boundaries before relying on the output.
