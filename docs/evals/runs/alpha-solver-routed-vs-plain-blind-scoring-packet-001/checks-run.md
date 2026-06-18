# Checks run

- `python - <<'PY' ... PY`: generated 12 scorer-facing blinded case files from the committed manual output files with blank scoring rows.
- `python - <<'PY' ... PY`: verified 12 blinded case files exist, each has Response A, Response B, blank scoring sheet, and `BLANK_NOT_SCORED`; verified no committed file in this packet contains source-directory or source-heading markers.
- `python -m pytest -q`: passed.
