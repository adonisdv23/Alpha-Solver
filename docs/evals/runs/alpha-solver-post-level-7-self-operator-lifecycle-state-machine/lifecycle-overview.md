# Lifecycle Overview

## Purpose

The Self Operator lifecycle is a future control plane model for bounded, auditable operator-assisted automation. It is designed to keep the system local-only unless and until an operator explicitly approves an externally visible action.

## Lifecycle shape

1. `created`: a proposed operator run exists as a record or plan.
2. `preflight`: local-only checks validate scope, permissions, evidence, credential boundaries, fallback boundaries, and claim safety.
3. `awaiting_operator_confirmation`: the run is ready to proceed but requires explicit operator approval.
4. `running_local_only`: approved local-only activity is in progress inside the documented boundary.
5. Terminal or stop states: `blocked`, `stopped`, `completed`, `failed`, and `archived`.

## Fail-closed rule

The lifecycle must fail closed into `blocked` or `failed` when any required safety condition is missing, stale, or ambiguous. Missing permission, missing evidence, unclear scope, missing credentials boundary, missing fallback boundary, or unsafe claims must never be treated as implicit approval.

## External visibility rule

The operator must approve all externally visible actions. A future implementation must not post, deploy, call hosted providers, update external systems, change public artifacts, send notifications, or promote evidence without explicit operator approval recorded before the action.
