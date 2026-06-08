# Prompt Pack Overview

## Draft status

This is a draft prompt pack for future implementation lanes. It is not an implementation plan approval, not a runbook execution, and not evidence that Self Operator MVP exists.

## Universal prompt header

Each future prompt should begin with this header:

```text
HARD STOP: Stop immediately unless a later authoritative Level 8 decision has accepted Self Operator readiness and selected implementation planning for this specific lane.

Scope is local-only. Do not call hosted providers. Do not use credentials. Do not use browser automation. Do not deploy. Do not create billing exposure. Do not expose or modify /v1/solve. Do not expose or modify dashboard behavior. Do not promote evidence. Do not run any prompt from this packet unless the future lane explicitly asks you to run that exact prompt.
```

## Prompt sequence intent

The prompts are intentionally separable so a future operator can authorize one narrow lane at a time:

- Prompt 01 drafts a concrete implementation plan.
- Prompt 02 adds or updates static tests.
- Prompt 03 implements local artifact schema code.
- Prompt 04 implements a local preflight runner.
- Prompt 05 implements approval capture.
- Prompt 06 implements stop-state handling.
- Prompt 07 implements a local harness wrapper.
- Prompt 08 executes acceptance checks locally.

## Non-execution rule

This packet drafts text only. The prompts below must not be executed as part of this packet.
