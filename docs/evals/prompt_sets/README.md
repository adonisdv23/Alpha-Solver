# Eval Prompt Sets

This directory stores versioned, repo-safe prompt manifests for Alpha Solver
evaluation work. Prompt manifests are documentation artifacts only; they are not
runtime prompt templates and do not change provider behavior.

## Current prompt sets

| Prompt set | Purpose | Human guide |
| --- | --- | --- |
| `higher_headroom_prompt_set_v1.md` | Higher-headroom Alpha-vs-plain comparison prompts for `OUTPUT-DIFFERENTIATION-PHASE-001`. | `docs/evals/HIGHER_HEADROOM_PROMPT_SET.md` |

## Safety rules

Prompt manifests must not include secrets, real API keys, bearer tokens,
dashboard passwords, cookies, CSRF tokens, session values, raw provider payloads,
provider account identifiers, private customer data, or sensitive personal data.
