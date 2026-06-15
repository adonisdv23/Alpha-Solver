# Interrupt and Follow-up Semantics

This document defines paper-only operator semantics for a future Alpha-native local operator harness. It does not implement runtime orchestration or UI behavior.

## Operator interrupt

An operator interrupt is an explicit instruction to stop the current action immediately and preserve the current evidence state. The session must record:

- who or what initiated the interrupt;
- the current task id and operator action;
- whether raw output exists;
- whether raw output is authorized to preserve;
- the stop reason;
- the next-safe-action.

An interrupt must not silently convert into a new provider call, model call, file operation, package install, external upload, or runtime exposure.

## Stop-condition

A stop-condition is a predeclared boundary that requires halting or escalation. Examples:

- missing operator authorization;
- request to use tokens, credentials, providers, hosted models, or local models;
- request to install packages or activate tools;
- request to expose dashboard, public API behavior, or `/v1/solve`;
- evidence conflict or missing raw output;
- needs-human/legal/safety/security/privacy boundary;
- attempt to make value, readiness, benchmark, provider, local-model, public-use, or Alpha superiority claims without evidence.

## Queued follow-up

A queued follow-up is a future task request recorded without execution. It should include:

- follow-up id;
- requested action;
- required authorization;
- required evidence inputs;
- blocked claims;
- proposed next-safe-action.

Queued follow-ups do not imply authorization. They are planning entries only.

## Approval gate

An approval gate is a required operator decision before crossing a boundary. Approval gates are required before any future:

- implementation;
- dependency or package change;
- Pi.dev experiment;
- provider or model call;
- credential or token use;
- dashboard, API, or `/v1/solve` exposure;
- Google Sheets or external-ledger mutation;
- benchmark, scoring, routing, council, registry, or comparison behavior.

## Evidence-review intervention

An evidence-review intervention is an operator action that pauses interpretation until provenance, raw-output pointers, score pointers, redaction state, and non-claims are checked. It should be used when a transcript, output, or summary could be mistaken for stronger evidence than it supports.
