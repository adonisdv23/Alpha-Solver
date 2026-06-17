# Stop conditions

Stop this lane or any later pilot lane if:

- source-of-truth docs disagree on the selected-next state,
- another open PR touches source-of-truth docs or the routed-vs-plain packet files,
- provider, hosted-model, local-model, tool, or web execution would occur without explicit later authorization,
- outputs would be generated in this authorization lane,
- scoring, unblinding, or raw prior-output inspection is requested,
- task ids would be changed,
- route metadata cannot be captured cleanly,
- blinding cannot be preserved,
- secrets, credentials, private data, or unsafe high-stakes requests appear,
- Google Sheets mutation, dependency addition, `/v1/solve` exposure, deployment, or public/demo behavior is requested, or
- any claim would imply readiness, benchmark success, production/public readiness, provider quality, local-model quality, tool quality, or Alpha superiority.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
