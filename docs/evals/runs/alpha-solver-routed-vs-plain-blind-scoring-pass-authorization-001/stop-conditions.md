# Stop Conditions

Stop immediately if any condition applies:

- Source identity or an A/B key is visible.
- Scoring would require source artifacts or route metadata.
- Source-of-truth docs do not match the PR #619 post-merge state before this prep lane begins.
- Any score, preference, or rationale is accidentally filled in this prep lane.
- Any scoring, unblinding, interpretation, runtime, provider, local-model, tool, web, or Sheets action is required.
