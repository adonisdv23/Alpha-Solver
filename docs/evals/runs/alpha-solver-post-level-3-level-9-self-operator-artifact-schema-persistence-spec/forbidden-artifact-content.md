# Forbidden artifact content

Artifacts must block and omit:

- secrets and credentials;
- provider outputs;
- billing data;
- external API responses;
- browser data;
- deployment output;
- evidence-promotion labels;
- source-artifact mutations;
- production route output;
- hosted model outputs.

If any forbidden content would be captured, the future lane must stop and write only a stop-state artifact with redaction markers.
