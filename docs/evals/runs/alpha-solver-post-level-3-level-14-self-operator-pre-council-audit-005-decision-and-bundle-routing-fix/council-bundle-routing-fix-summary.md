# Council bundle routing fix summary

This lane clarifies the derivative Council audit evidence bundle in three places:

1. `selected-next-lane.md` now states that the bundle is clean after required preparation-lane checks only and that Council has not run.
2. `blocker-fallback-lane.md` now routes a pre-manual-Council bundle block to the fix lane first, reserving fallback only for cases where the fix lane cannot proceed or the bundle cannot be safely repaired.
3. `current-state-snapshot.md` receives a post-audit amendment instead of rewriting the original snapshot.

The manual Council run lane remains a future lane. This lane did not run Council.
