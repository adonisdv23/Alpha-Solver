# Non-Production Runner Contract

## Contract

The non-production local orchestration runner is an internal or CLI-callable path for exercising local LLM orchestration without production exposure.

## Required behavior

The runner must:

1. require explicit local LLM operator opt-in;
2. invoke only the localhost or loopback local runtime backend;
3. require no provider keys;
4. use finite timeouts;
5. avoid hosted fallback;
6. fail closed on runtime, parse, echo, empty-output, or timeout errors;
7. normalize successful bounded output into an Alpha-style result;
8. preserve runtime metadata and `behavior_evidence=false`.

## Not authorized

This runner does not authorize production `/v1/solve`, dashboard preview, provider fallback, billing path changes, model-quality claims, or evidence-model promotion.
