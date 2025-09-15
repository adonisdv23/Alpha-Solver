import json
from pathlib import Path
from typing import Iterable, List, Dict


def load_jsonl(path: Path, required_fields: Iterable[str]) -> List[Dict]:
    """Load a JSONL file and validate required fields."""
    items: List[Dict] = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            missing = [f for f in required_fields if f not in obj]
            if missing:
                raise ValueError(f"Missing fields {missing} in {obj}")
            items.append(obj)
    ids = [item['id'] for item in items]
    if ids != sorted(ids):
        raise ValueError('Dataset ids must be sorted')
    return items
