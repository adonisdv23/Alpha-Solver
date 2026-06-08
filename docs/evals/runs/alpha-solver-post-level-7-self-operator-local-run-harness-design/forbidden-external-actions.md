# Forbidden External Actions

## Absolute prohibition

The future local run harness described by this packet is strictly local-only. It must use absolute no-provider-call behavior. It must not include any exception, fallback, or interpretation that allows provider calls inside this local harness.

Forbidden actions include:

- no provider calls
- no hosted model calls
- no external API calls
- no fallback
- no credential use
- no billing
- no dashboard exposure
- no /v1/solve exposure
- no browser automation
- no deployment
- no evidence promotion

## Additional forbidden actions

The local harness must also not:

- run local models;
- run hosted models;
- run Ollama;
- configure credentials or secrets;
- add provider routing;
- add provider fallback;
- add hosted fallback;
- expose or call `/v1/solve`;
- expose dashboards;
- run benchmarks;
- perform billing work;
- deploy;
- control browsers;
- promote evidence.

## Future provider-aware clarification

A future lane may separately design provider-aware behavior, but this local run harness design must not be read as authorizing provider calls. The local harness may only perform bounded local preflights, local artifact capture, local docs/checker commands, and future local-only tasks explicitly authorized by a later implementation lane.
