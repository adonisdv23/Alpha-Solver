# Release Gate Checker Summary

The checker evaluates eleven deterministic gates and emits a JSON report with:

- gate ID;
- status (`pass`, `blocked`, `missing`, or `needs_review`);
- evidence path;
- reason;
- required next action.

The final status is selected from the approved release-control vocabulary only. The report does not use forbidden MVP-readiness wording and does not claim readiness. If any gate is incomplete, the checker reports a blocked status.
