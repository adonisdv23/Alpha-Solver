# Operator-Visible Routing Decisions

## Operator visibility principle

Future routing decisions must be visible to operators before provider execution when the decision can affect data egress, cost, safety posture, evidence status, runtime behavior, or product-surface exposure.

## Minimum visible fields

A future operator-visible routing decision should display or log:

- selected route state: selected provider, no-provider stop, or blocked;
- provider and model identifier when applicable;
- request/task class;
- environment and surface where the decision applies;
- eligible providers considered;
- providers excluded and exclusion reasons;
- selected provider reason;
- capability matching result;
- safety gate result;
- budget/spend gate result;
- data-egress posture;
- fallback/retry authorization state;
- evidence status and promotion boundary;
- operator confirmation status;
- stop condition if no provider is selected.

## Before/after visibility

- **Before execution**: operators should see the selected route state, data egress posture, budget gate, safety gate, and fallback/retry authorization.
- **After execution**: operators should see the actual provider used, whether any fallback/retry occurred, final evidence status, and any stop/override reason.

## Explainability requirement

Future routing must produce a concise explanation that a non-implementing operator can understand. The explanation should distinguish capability fit, safety gate results, budget gate results, operator authorization, and availability.
