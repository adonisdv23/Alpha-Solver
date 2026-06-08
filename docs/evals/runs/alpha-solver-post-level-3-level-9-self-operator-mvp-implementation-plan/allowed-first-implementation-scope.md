# Allowed first implementation scope

The future first-code lane may only implement a static test scaffold. The allowed work is:

- add static tests for prohibited Self Operator behavior;
- add inert fixtures used only by those tests;
- add static finding IDs and expected failure assertions inside the test scaffold;
- document raw artifacts and reviewer notes produced by the future implementation run;
- run local offline checks required by the future lane.

The future first-code lane is local-only and operator-supervised. It must have no provider calls, no hosted model calls, no external API calls, no credentials, no browser automation, no deployment, no billing, no route exposure, no fallback, and no evidence promotion.
