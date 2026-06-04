# Local LLM Contract-Consumption Proof Review Gate

Lane ID: `ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-REVIEW-GATE-001`

## Purpose

This docs-only lane prepares the merge-review gate for the future proof lane
`ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001`.

The future proof lane is expected to show that `alpha_solver_portable.py` can be
loaded, fingerprinted, and consumed as the prompt contract in a fake
local-LLM-style request without calling real models, Ollama, provider adapters,
or runtime API paths.

## Source Readiness Lane

This review gate follows source readiness lane PR #281, which completed
`ALPHA-LOCAL-LLM-PREVIEW-READINESS-001` and recommended a contract-consumption
proof before any full local LLM provider implementation.

## What This Review Gate Checks

A reviewer should use this gate to confirm that the future proof PR:

- consumes `alpha_solver_portable.py` as the source prompt contract;
- preserves the prompt source path and fingerprint as evidence metadata;
- uses a fake client to construct a local-LLM-style request only;
- keeps system or instruction content separate from the user prompt;
- treats fake-client output as non-behavior evidence;
- fails closed when contract loading, fingerprinting, fake-client execution, or
  output hygiene checks fail;
- keeps `MODEL_PROVIDER=local` smoke-only;
- adds focused tests for the proof surface; and
- avoids readiness, validation, superiority, production, MVP, `/v1/solve`, or
  provider-orchestration claims.

## What This Review Gate Does Not Do

This lane does not:

- implement local LLM support;
- implement or expand an Ollama adapter;
- call Ollama, local models, hosted models, or provider APIs;
- call `_tree_of_thought`;
- use `alpha-solver-v91-python.py` for generation;
- change runtime behavior, routing, model configuration, provider adapters, or
  `/v1/solve`;
- run operator tests;
- import operator results;
- score, rescore, or generate model outputs;
- start Batch C; or
- make Alpha quality, runtime readiness, product readiness, validation,
  superiority, or production claims.

## Evidence Boundaries

Evidence accepted by this gate is limited to docs, focused proof metadata, and
future tests that demonstrate portable contract consumption through a fake
client. Fake-client evidence is non-behavior evidence: it may prove wiring,
metadata preservation, failure behavior, and prompt-source separation, but it
must not be described as local LLM quality evidence or runtime readiness.
