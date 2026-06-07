# Local LLM Solver Orchestration Operator Guide

## Purpose

This guide explains how a Level 2 operator may use the local LLM solver orchestration path as a local-only development capability after final track closeout. It is practical usage guidance for inspecting the existing non-production runner, its normalized result shape, and its diagnostic metadata.

## Level 2 boundary

Level 2 use means local developer-machine operation only. The path is default-off, requires explicit local opt-in, uses a localhost or loopback Ollama-style endpoint, requires no hosted provider keys, and preserves `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.

This guide does not reinterpret the final closeout packet and does not broaden the evidence boundary. The controlling source remains the local LLM solver orchestration closeout/readiness packet and the implementation contracts in `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` and `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`.

## Operator guidance, not validation

This guide is not validation, smoke evidence, benchmark evidence, model-quality evidence, provider orchestration evidence, production readiness, MVP readiness, `/v1/solve` readiness, dashboard readiness, billing evidence, broad runtime readiness, Alpha superiority, or evidence-model promotion.

## Start here

- Use [quick-start.md](quick-start.md) for the shortest safe local sequence.
- Use [command-reference.md](command-reference.md) for exact command templates and the current operator-command status.
- Use [safe-use-boundaries.md](safe-use-boundaries.md) and [non-claims-and-blocked-uses.md](non-claims-and-blocked-uses.md) before preserving or sharing any output.
