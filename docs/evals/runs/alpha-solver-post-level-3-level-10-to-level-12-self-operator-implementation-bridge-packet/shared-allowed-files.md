# Shared allowed file categories for future lanes

These categories are planning boundaries, not forced file paths. Future lane prompts must narrow them before implementation.

Allowed future categories may include:

- local-only schema helpers;
- local-only artifact writers/readers;
- local-only preflight classification helpers;
- local-only approval record helpers;
- local-only stop-state record helpers;
- local-only dry-run harness wrapper;
- deterministic tests;
- inert fixtures;
- lane-completion docs packets.

Each future lane must prove changed-file scope before commit and PR creation. The default is to split any lane whose changed files make review broad or ambiguous.
