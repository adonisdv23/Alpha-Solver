# Abort conditions

A future repeatability execution lane must abort before or during execution if
any condition below is true:

1. current checkout is not the intended merged main state;
2. PR #480, PR #481, or PR #482 is not present in merged history;
3. the first supervised-use review packet is missing;
4. the first supervised-use review decision is not
   `accepted_for_limited_repeatability_review`;
5. the first supervised-use review does not select this packet lane;
6. unresolved P0, P1, or P2 findings are present in the first-use review packet;
7. the final local status CLI is implemented before the repeatability lane;
8. exact operator confirmation is absent or mismatched;
9. no fresh run ID is provided;
10. output root is not fresh, outside the repository, and empty or newly created;
11. the executable plan contains `git fetch`;
12. the executable plan contains unsafe root handling such as `Path("$ROOT")`;
13. a quoted heredoc relies on shell expansion inside Python rather than reading
    `os.environ["ROOT"]`;
14. any forbidden surface is requested, attempted, or cannot be disproved;
15. any source-artifact mutation is requested or detected;
16. any command deviates from the verified execution plan.

Abort means no repeatability run proceeds. The future lane must record the abort
state and select the blocked or fallback lane as applicable.
