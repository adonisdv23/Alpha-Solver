import json
from typing import Iterable, List, Optional, Sequence, TextIO


def export(
    entries: Iterable[dict],
    fp: TextIO,
    *,
    start_ts: Optional[float] = None,
    end_ts: Optional[float] = None,
    event_types: Optional[Sequence[str]] = None,
    tenant_id: Optional[str] = None,
) -> dict:
    """Export audit log entries to JSONL with optional filtering.

    Args:
        entries: iterable of entries.
        fp: file-like object to write JSON lines to.
        start_ts, end_ts: inclusive time window.
        event_types: sequence of event types to include.
        tenant_id: only include entries matching this tenant.
    Returns:
        Manifest dict containing ``count`` and ``head``/``tail`` hashes.
    """
    filtered: List[dict] = []
    for e in entries:
        if start_ts is not None and e["ts"] < start_ts:
            continue
        if end_ts is not None and e["ts"] > end_ts:
            continue
        if event_types is not None and e["type"] not in event_types:
            continue
        if tenant_id is not None and e.get("tenant_id") != tenant_id:
            continue
        filtered.append(e)

    filtered.sort(key=lambda x: (x["ts"], x["id"]))
    for e in filtered:
        fp.write(json.dumps(e, sort_keys=True) + "\n")

    manifest = {"count": len(filtered), "head": None, "tail": None}
    if filtered:
        manifest["head"] = filtered[0]["hash"]
        manifest["tail"] = filtered[-1]["hash"]
    return manifest
