# Routing Policy Overview

## Policy purpose

Future provider routing must be explicit, explainable, operator-visible, and safety-bounded. Routing must be treated as a policy decision, not as an incidental implementation detail hidden inside runtime/provider/API/dashboard code.

## Future routing requirements

Any future routing implementation proposal must define:

1. **Decision authority**: which Level 7 approval or downstream implementation contract authorizes use of this packet.
2. **Routing scope**: which request classes, provider classes, environments, and product surfaces are in scope.
3. **Selection inputs**: the exact inputs used to choose a provider or stop selection.
4. **Capability matching**: the required mapping from task needs to provider/model capabilities.
5. **Safety-first rules**: conditions that prefer safe stop over provider selection.
6. **Operator visibility**: the routing decision fields visible to operators before and after execution.
7. **No implicit routing**: a guarantee that provider choice is not inferred from ambient configuration, import order, availability alone, or hidden fallback.
8. **Stop conditions**: explicit conditions that prevent selection, execution, fallback, or retry.

## Required future route decision shape

A future route decision should be represented as a structured decision record before execution. At minimum, it should identify:

- request class;
- operator-approved environment;
- eligible provider set;
- excluded provider set with reasons;
- selected provider or stop state;
- required capability match;
- safety and budget gates evaluated;
- fallback/retry authorization state;
- operator-visible explanation;
- evidence boundary and promotion status.

## Level 7 control

Level 7 controls whether and how this packet is used. Nothing in this packet activates routing, chooses a provider, approves provider calls, or authorizes exposure of a product/API/dashboard surface.
