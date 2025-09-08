# Router v12

Router v12 introduces deterministic branch ordering and token-budget pruning.
Branches are sorted by score with a tie-breaker hash derived from a seed and the
branch id. A configurable token budget prunes low-utility branches early and the
router emits telemetry summarising the decision.

Optional majority voting can be enabled for low-confidence scenarios; it uses a
simple deterministic majority over `k` answers. All features can be disabled via
configuration to preserve backwards compatibility.
