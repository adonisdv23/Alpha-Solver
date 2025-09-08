# Tiny Telemetry Web Viz

`viz/index.html` is a single-file visualization for telemetry JSONL logs.

1. Open the file in a browser.
2. Paste JSONL text or drag a log file onto the page.
3. Charts will render showing run summaries, layer scores and SAFE-OUT routes.
4. Use the **Export** button to download a static PNG snapshot.

This viewer uses only vanilla JavaScript and inline CSS so it can be attached to
CI artifacts without a build step.
