# High-Risk Non-Exposure Summary

Blocked or failed-closed high-risk outputs must not expose unsafe model-produced operational guidance in normal result fields.

The fix strips considerations and assumptions for high-risk block outcomes and other pass-one block outcomes that do not satisfy deterministic safe overrides.

Unsafe guidance covered by focused tests includes requests or model output involving:

- disabling safety monitoring;
- hiding changes from reviewers;
- avoiding logs;
- preventing alerts;
- disabling automated checks;
- hiding audit trail activity.

Blocked high-risk outputs continue to return empty `answer` and `final_answer` fields.
