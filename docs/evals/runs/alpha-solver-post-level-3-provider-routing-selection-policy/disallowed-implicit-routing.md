# Disallowed Implicit Routing

## Purpose

Provider routing must not happen implicitly. Any future provider selection must be explicit, policy-governed, operator-visible, and bounded by stop conditions.

## Disallowed implicit routing behaviors

Future work must not select or call a provider based on:

- provider import order;
- first provider found in configuration;
- first endpoint that responds;
- silent fallback after provider failure;
- local environment variables alone;
- credential presence alone;
- dashboard or API default values alone;
- runtime convenience paths;
- hidden model aliases;
- stale previous run metadata;
- benchmark scores without safety and operator gates;
- billing availability alone;
- cost or speed alone;
- broad provider class labels without capability matching.

## Disallowed hidden fallback

Fallback must not be implicit. If future fallback is ever proposed, it must be separately authorized, operator-visible, bounded, logged, and subject to the same capability matching, safety-first selection, budget, and stop-condition requirements as primary selection.

## Disallowed runtime activation

This packet does not implement routing and does not call providers. It does not authorize runtime/provider/API/dashboard files to select providers, expose `/v1/solve`, add fallback, run models, run benchmarks, perform billing work, or promote evidence.
