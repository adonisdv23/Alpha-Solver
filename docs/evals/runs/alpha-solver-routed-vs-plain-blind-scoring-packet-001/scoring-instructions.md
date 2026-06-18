# Future scoring instructions

A future separately authorized scorer may review only the blinded case files in `blinded-cases/` and the frozen rubric. The scorer must leave source identity unknown while scoring.

Required future scoring fields per case and response:

- dimension scores from 0 to 3 for each frozen rubric dimension;
- concise notes for material defects or strengths;
- contested-score flag if the scorer is uncertain;
- scorer identity/tooling statement;
- scoring timestamp;
- score-lock confirmation.

This packet does not authorize the future scorer to inspect source directories, route metadata, source maps, unblinding materials, Git history for source identity, provider dashboards, local model outputs, `/v1/solve`, Google Sheets, or any external/current research.
