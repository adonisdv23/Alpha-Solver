# Stop before editing

A future first code lane must stop before editing any file if one or more of these conditions is true:

1. Level 8 has not been accepted in the controlling decision record.
2. A concrete implementation lane has not been selected by the controlling decision record.
3. The working branch is not current-main-based.
4. The requested edit would exceed the allowed scope of the selected code lane.
5. The requested edit introduces or requires provider call risk.
6. The requested edit introduces or requires credential risk.
7. The requested edit introduces or requires browser automation.
8. The requested edit introduces or requires deployment.
9. The requested edit introduces or requires billing work.
10. The requested edit introduces or requires an external API.
11. The requested edit exposes or changes `/v1/solve` or dashboard behavior.
12. The requested edit promotes evidence beyond its accepted boundary.
13. The requested edit modifies source artifacts.

When any stop condition applies, the future operator must leave the working tree unchanged and report the blocker instead of editing.
