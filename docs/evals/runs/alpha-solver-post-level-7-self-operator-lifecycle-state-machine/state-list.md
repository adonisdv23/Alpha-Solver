# State List

## `created`

A run request or lifecycle record has been created. No work is authorized beyond local preflight evaluation.

## `preflight`

The system performs local-only checks for authorization, scope, evidence, credentials boundary, fallback boundary, and unsafe claims. Preflight must not call providers, deploy, or perform externally visible actions.

## `awaiting_operator_confirmation`

Preflight passed and the system is waiting for explicit operator confirmation. No externally visible action is authorized in this state.

## `running_local_only`

The approved activity is running only inside the local documented boundary. Any new external action, scope expansion, credential use, fallback change, or claim promotion returns control to `awaiting_operator_confirmation` or fails closed.

## `blocked`

A recoverable blocking condition prevents safe progress. Typical reasons include missing permission, missing evidence, unclear scope, missing credentials boundary, missing fallback boundary, unsafe claims, unavailable prerequisites, or required operator approval not yet granted.

## `stopped`

The operator or system intentionally stopped the run before completion. A stopped run must not resume automatically without a new approval path.

## `completed`

The approved local-only work completed inside the evidence boundary. Completion does not imply deployment, production readiness, provider readiness, benchmark success, or evidence promotion.

## `failed`

The run reached a non-recoverable failure or safety violation. Failure requires audit capture and cannot transition back to active execution automatically.

## `archived`

The run record is preserved for audit and historical review. Archived records are immutable except for clearly marked archival metadata corrections.
