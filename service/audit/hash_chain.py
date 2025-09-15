import hashlib
import json
from typing import Dict, Iterable, Optional

ZERO_HASH = "0" * 64


def _canonical_json(data: Dict) -> str:
    """Return a deterministic JSON string for hashing."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def compute_hash(entry: Dict, prev_hash: str) -> str:
    """Compute the SHA256 hash of the entry chained with ``prev_hash``."""
    to_hash = _canonical_json(entry) + prev_hash
    return hashlib.sha256(to_hash.encode("utf-8")).hexdigest()


def verify_chain(entries: Iterable[Dict]) -> Optional[int]:
    """Verify integrity of a hash chain.

    Args:
        entries: iterable of audit log entries ordered by ``id``.
    Returns:
        ``None`` if the chain is valid, otherwise the index of the first corrupt
        entry.
    """
    prev_hash = ZERO_HASH
    for idx, entry in enumerate(entries):
        # reconstruct entry without the ``hash`` field for recomputation
        body = {k: v for k, v in entry.items() if k != "hash"}
        expected = compute_hash(body, prev_hash)
        if entry.get("prev_hash") != prev_hash or entry.get("hash") != expected:
            return idx
        prev_hash = entry["hash"]
    return None
