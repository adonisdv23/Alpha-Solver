from __future__ import annotations

from typing import Dict, List

DEFAULT_FIELDS = [
    "decision",
    "confidence",
    "budget_verdict",
    "tool",
    "score",
    "sandbox_decision",
]


# ---------------------------------------------------------------------------
def _is_secret(key: str) -> bool:
    key_lower = key.lower()
    if key_lower == "pii_raw":
        return True
    return key_lower.endswith("_token") or key_lower.endswith("_secret")


def normalize(event: Dict, *, keep_keys: List[str]) -> Dict:
    """Return a normalized view of *event*.

    Only keys from ``keep_keys`` plus the default fields are kept. Any float
    values are rounded to four decimal places. Keys containing potential PII
    such as ``pii_raw`` or those ending in ``_token`` or ``_secret`` are
    removed.
    """

    allowed = set(DEFAULT_FIELDS) | set(keep_keys)
    out: Dict = {}
    for key in allowed:
        if key not in event:
            continue
        if _is_secret(key):
            continue
        value = event[key]
        if isinstance(value, float):
            value = round(value, 4)
        out[key] = value
    return out


# ---------------------------------------------------------------------------
def diff_lists(
    a: List[Dict],
    b: List[Dict],
    *,
    id_key: str = "id",
    keys: List[str],
) -> List[str]:
    """Return deterministic textual diffs between two lists of events.

    ``a`` and ``b`` are lists of dicts. Events are paired by ``id_key`` and the
    specified ``keys`` are compared. The output is sorted by id ascending and is
    limited to 200 lines. When more mismatches are present, a final line
    ``"... (truncated)"`` is appended.
    """

    keep = list(set(keys) | {id_key})
    a_map = {e[id_key]: normalize(e, keep_keys=keep) for e in a if id_key in e}
    b_map = {e[id_key]: normalize(e, keep_keys=keep) for e in b if id_key in e}

    ids = sorted(set(a_map) | set(b_map))
    lines: List[str] = []
    mismatch_count = 0
    limit = 200

    for eid in ids:
        ea = a_map.get(eid)
        eb = b_map.get(eid)
        if ea is None or eb is None:
            mismatch_count += 1
            if len(lines) < limit:
                side = "a" if ea is None else "b"
                lines.append(f"id={eid} missing in {side}")
            continue
        for key in keys:
            va = ea.get(key)
            vb = eb.get(key)
            if va != vb:
                mismatch_count += 1
                if len(lines) < limit:
                    lines.append(f"id={eid} {key}: {va} != {vb}")

    if mismatch_count > len(lines):
        if len(lines) > limit:
            lines = lines[:limit]
        lines.append("... (truncated)")
    return lines
