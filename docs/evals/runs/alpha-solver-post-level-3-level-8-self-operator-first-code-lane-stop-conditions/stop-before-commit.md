# Stop before commit

A future first code lane must stop before committing if review of the working tree shows any of these conditions:

- Level 8 acceptance is absent or ambiguous.
- The selected lane is not an implementation lane.
- The branch is not current-main-based.
- Changed files exceed the allowed scope for the selected lane.
- Any diff indicates provider call risk, credential risk, browser automation, deployment, billing, external API behavior, `/v1/solve` exposure, dashboard exposure, evidence promotion, or source artifact modification.

If any condition is found after edits have already occurred, the future operator must not commit and must report the condition. The operator must not use a commit to normalize or hide an out-of-scope diff.
