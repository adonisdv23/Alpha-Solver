# Non-Actions

This lane did not and must not:

- call providers;
- use provider tokens or credentials;
- access credentials or billing;
- run hosted models through product/runtime code;
- run or install local models;
- expose `/v1/solve`;
- expose dashboard behavior or public API behavior;
- modify runtime, API, dashboard, routing, council, benchmark, or scoring code;
- mutate Google Sheets or any external ledger;
- score outputs, fill blind scores, unblind outputs, or create final interpretation;
- create or commit an operator-only unblinding map;
- add dependencies.
