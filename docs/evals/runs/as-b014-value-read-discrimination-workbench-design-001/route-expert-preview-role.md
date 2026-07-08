# Route / Expert Preview Role

## Role

Route/expert preview is a diagnostic component of `VALUE_READ_DISCRIMINATION_WORKBENCH`, not the whole product.

## When useful

It is useful when a packet includes route metadata, task interpretation, expert/persona selection, SAFE-OUT, confidence, shortlist, or fallback context that helps explain why the Alpha/routed side differs from a plain/baseline output.

## When missing

It is missing when no committed route metadata exists, when route metadata was out of scope for the packet, or when the packet is a pure case/scoring/interpretation artifact. Missing route metadata should be shown as `missing`, `unavailable`, or `out of scope`, not silently inferred.

## How it helps discrimination

It helps the operator ask whether the output difference is connected to Alpha Solver-specific routing and evidence behavior rather than a generic prompt difference. It can show the presence or absence of task interpretation, route choice, expert framing, SAFE-OUT handling, confidence posture, shortlist options, and fallback state.

## Why it does not prove quality

Route/expert preview is metadata. It does not show that the answer is correct, valuable, safer, or superior. It only helps explain context for a bounded comparison.

## Representation

- SAFE-OUT: present, absent, not triggered, blocked, or out of scope.
- Confidence: present, missing, unavailable, or out of scope.
- Shortlist/fallback: present, absent, unavailable, or out of scope.
- Route/expert/persona: present with source path, missing, or out of scope.

## Difference from a live execution cockpit

The preview reads committed artifacts. It must not run providers, hosted models, local models, tools, web browsing, `/v1/solve`, CLI/subprocesses, queues, schedulers, workers, or background jobs.
