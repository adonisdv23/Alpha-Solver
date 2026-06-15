# ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001 · Needs-Human Escalation Protocol

Status: `SPEC_OK`

Lane ID: `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001`

## Purpose

Define a docs-only escalation protocol for Alpha Solver outputs where refusal, uncertainty, missing context, or evidence conflict should become a useful operator outcome rather than a dead end.

## Scope

This protocol covers product-facing answer behavior and Value Read scoring notes for synthetic or future authorized evaluations. It does not implement runtime routing, call providers, collect private data, or create domain-specific legal, medical, financial, safety, or credential instructions.

## Required behavior

Alpha Solver should surface `needs_human: true` only when the available context makes automated completion unsafe, unsupported, unauthorized, or materially under-evidenced. Escalation should not be treated as always correct; unnecessary escalation can reduce answer quality and discrimination scores.

The detailed operator-facing protocol is captured in `docs/evals/runs/alpha-solver-escalation-needs-human-protocol-001/README.md`.
