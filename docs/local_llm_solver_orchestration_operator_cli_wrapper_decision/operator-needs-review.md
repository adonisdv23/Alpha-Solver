# Operator Needs Review

## Level 2 operator need

A Level 2 operator needs a repeatable way to invoke the existing local solver orchestration path from a developer machine without copying a multi-line Python snippet for every local run. The operator also needs a surface that makes safety-critical settings explicit:

- local LLM mode remains default-off;
- the operator must opt in explicitly;
- endpoint input must remain localhost or loopback only;
- timeout must be finite;
- hosted provider keys must not be required;
- hosted fallback must not occur;
- result output must preserve `behavior_evidence=false`;
- no `/v1/solve` or dashboard path may be introduced.

## Why the module entry point alone is not ideal for operators

The Python/module entry point is precise and testable, but it asks operators to write or copy Python. That raises avoidable usability and consistency issues for a Level 2 usage path:

- operators may alter templates while trying to run the function;
- output capture and JSON formatting are not standardized by a stable command;
- invocation mistakes can obscure whether a failure came from configuration, endpoint validation, timeout validation, or model output handling;
- the absence of a named command makes future operator runbooks harder to keep consistent.

## Why the need does not justify broad exposure

The operator need is only a local usability need. It does not justify production routing, API exposure, dashboard exposure, hosted provider fallback, provider orchestration, benchmark claims, model-quality claims, billing changes, MVP readiness, production readiness, or evidence-model promotion.
