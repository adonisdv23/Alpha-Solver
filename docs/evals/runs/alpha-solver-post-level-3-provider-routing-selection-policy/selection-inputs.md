# Selection Inputs

## Required explicit inputs

Future provider selection must use only explicit, reviewable inputs. At minimum, a proposed implementation contract must identify whether each input is required, optional, operator supplied, policy supplied, or derived.

Required future input categories:

- **Task intent**: the task family, expected output type, and whether the task is evaluation, operator-assist, production-facing, or diagnostic.
- **Capability requirements**: model/provider capabilities required for the task, including context length, tool permissions, structured output support, determinism controls, locality expectations, and safety controls.
- **Data sensitivity**: whether the input includes private, regulated, customer, credential, source, evaluation, or embargoed evidence.
- **Environment**: local-only, hosted-provider-allowed, offline, CI, manual-operator, or production-like context.
- **Operator authorization**: explicit operator approval state for provider class, network use, spend, data egress, and evidence promotion.
- **Budget constraints**: maximum spend, token/compute caps, retry limits, and billing status.
- **Availability state**: provider health and readiness only as a gating input, never as the sole selection input.
- **Safety gates**: prohibited data, missing consent, unsafe prompt class, missing capability proof, or unreviewed evidence.
- **Evidence status**: whether the route is producing draft output, non-promotional evidence, or reviewed evidence eligible for a later promotion decision.

## Inputs that must not select providers by themselves

The following must not independently select a provider:

- first configured provider;
- first importable adapter;
- first reachable endpoint;
- lowest cost alone;
- fastest response alone;
- largest context window alone;
- provider popularity;
- environment variable presence alone;
- previous successful run alone;
- dashboard default alone;
- hidden fallback from a failed provider.

## Input recording requirement

Future implementations must record the inputs used for a routing decision in an operator-readable form. If an input is unavailable, stale, contradictory, or outside policy, selection must stop rather than infer a provider.
