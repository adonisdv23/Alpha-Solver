# Reviewability Requirements

## Reviewer expectations

Before any product surface relies on this packet, reviewers should be able to verify:

- which run ID applies, or that no run-scoped packet applies;
- which request ID identifies the attempted request;
- which trace records exist for the request path;
- which decision log entries explain allow, block, route, retry, escalation, or rejection outcomes;
- which error log entries identify failure categories and recovery state;
- which evidence references support review without promoting claims;
- which retention boundary applies;
- which redaction state applies;
- whether Level 6 accepted, amended, superseded, or rejected use of this packet.

## Reviewability requirements

- Records must be internally linkable by run ID, request ID, trace ID, decision log reference, error log reference, and evidence reference.
- Review must be possible without calling providers, running models, running benchmarks, or performing billing work.
- Review must identify missing, stale, contradictory, or overbroad observability artifacts as blockers.
- Review must preserve the distinction between documentation design and implemented runtime behavior.
