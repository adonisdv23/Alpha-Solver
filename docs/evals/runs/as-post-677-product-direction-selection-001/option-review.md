# Option Review

| Option | Core job | Alignment | Risk | Decision | Reason |
|--------|----------|-----------|------|----------|--------|
| Bounded smoke-test cockpit | Run one bounded smoke test with preview and receipt | Medium | Can be mistaken for product validation | Defer | Useful support surface, but not core product proof. |
| Value Read / discrimination workbench | Manage evidence, case packets, captured outputs, comparison, and operator decisions | High | Must avoid overstating value | Select | Strongest north-star alignment. |
| Route and expert-preview surface | Inspect routing, expert choice, SAFE-OUT, confidence, and boundaries | High | Could become isolated diagnostics | Defer as component or later lane | Best included in the workbench or split into a later focused lane. |
| CLI/artifact operator companion | Help inspect local artifacts and receipts | Medium | Could stay too technical | Defer as support infrastructure | Useful, but not the primary product direction. |
| Full real-run Operator Cockpit | Prepare, run, review, and receipt live model work | Medium | High drift toward generic prompt runner | Defer | Too broad without separate execution authorization and product boundaries. |
| Read-only status checkpoint | Show repository and console status | Low to medium | Operator usability already failed | Do not select | Already built enough for current evidence needs. |
