# Test Plan

Required checks:

- `git diff --check`
- `python -m py_compile tools/operator_test_console.py tests/test_operator_test_console.py`
- `python -m pytest -q tests/test_operator_test_console.py`
- Source-of-truth consistency review
- Changed-Markdown claim-safety review
- Changed-line forbidden-surface review

Router tests are not required because router code was not changed.
