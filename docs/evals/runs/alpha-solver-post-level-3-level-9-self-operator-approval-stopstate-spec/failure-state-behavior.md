# Failure-state behavior

On any blocked condition, the future implementation must:

- stop immediately;
- avoid continuing with partial implementation;
- avoid hiding out-of-scope diffs;
- avoid commit and PR creation unless the authorized lane explicitly allows a stop-state-only docs artifact;
- preserve local raw artifacts and reviewer notes;
- require operator review before any retry.
