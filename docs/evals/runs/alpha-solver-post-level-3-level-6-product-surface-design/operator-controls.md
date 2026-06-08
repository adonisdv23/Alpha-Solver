# Operator Controls

## Default-off requirements

Future product-surface controls must be default-off for:

- any `/v1/solve` exposure;
- dashboard publication or route exposure;
- hosted provider calls;
- paid provider calls;
- provider fallback;
- billing, quota, metering, or account features;
- benchmark execution;
- evidence promotion.

## Opt-in gates

Any future opt-in must require an explicit operator action, a documented purpose, an evidence-boundary acknowledgement, and an audit record. Environment defaults, implicit discovery, silent fallback, or automatic enablement are not acceptable opt-in mechanisms.

## Audit requirements

Future product surfaces must record:

- who or what initiated the action;
- timestamp and configuration snapshot;
- selected mode and enabled controls;
- evidence boundary acknowledged by the operator;
- provider or local runtime selected, if any;
- stop reason or completion status;
- redaction status;
- artifact paths or identifiers.

## Operator clarity requirement

If an operator cannot determine whether a control exposes an API, exposes a dashboard, calls a provider, bills money, runs inference, scores outputs, or promotes evidence, the lane must stop.
