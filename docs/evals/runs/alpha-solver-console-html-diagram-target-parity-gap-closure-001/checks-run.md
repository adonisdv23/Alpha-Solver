# Checks Run

| Check | Result | Notes |
|---|---:|---|
| `curl -L --fail --silent --show-error -o /tmp/alpha_solver_capability_guide.html https://github.com/user-attachments/files/29115017/alpha_solver_capability_guide.1.html` | Pass | HTML target artifact was accessible for target-context comparison only. |
| GitHub CLI live PR/issue checks | Unavailable | `gh` is not installed and `git remote -v` returned no remote metadata in this environment; per trigger, this was recorded and was not treated as a blocker by itself. |
| Open PR conflict check | Unavailable | Could not verify open PR file conflicts through GitHub CLI or remote metadata. Work proceeded under the trigger's GitHub-CLI-unavailable exception. |
| `git diff --check` | Pass | No whitespace errors. |
| `python -m py_compile tools/operator_test_console.py tests/test_operator_test_console.py` | Pass | Console and focused tests compile. |
| `python -m pytest -q tests/test_operator_test_console.py` | Pass | 62 passed; pytest reported existing deprecation warnings from FastAPI/Starlette under Python 3.14. |
| Source-of-truth consistency review | Pass | Rerun after blocker feedback on 2026-06-18. New lane and selected next state are present in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`; `docs/EVIDENCE_INDEX.md` no longer presents `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001` as the current selected state. |
| Changed-Markdown claim-safety review | Pass | Rerun after blocker feedback on 2026-06-18. Added Markdown lines were reviewed for unsupported broad claims. |
| Changed-line forbidden-surface review | Pass | Rerun after blocker feedback on 2026-06-18 using changed-line diff scope. Console/test added lines were reviewed for forbidden runtime/web/tool/API/Sheets surfaces. |

Router tests were not run because router code was not changed.
