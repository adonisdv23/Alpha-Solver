# Blinding rules

- Assign blind labels per task before scorer-facing packaging.
- Store the label-to-identity map outside scorer-facing materials.
- Do not commit secrets, credentials, private raw data, or sensitive unredacted outputs.
- Do not unblind in the output-collection lane unless a separate unblinding lane is explicitly authorized.
- Do not inspect raw prior outputs in this authorization lane.
- Route metadata may be captured for audit, but scorer access to route metadata requires a separately stated scoring design.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
