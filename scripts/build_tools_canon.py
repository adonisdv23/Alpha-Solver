import csv
import json
from pathlib import Path

REGISTRY_TOOLS = Path('registries/tools.json')
REGISTRY_SEED = Path('registries/registry_seed_v0_7_0.jsonl')
ARTIFACT_DIR = Path('artifacts')
ARTIFACT_DIR.mkdir(exist_ok=True)

COLUMNS = ['key', 'id', 'vendor_id', 'router_value', 'tier', 'category', 'popularity', 'sentiment']


def _load_tools_file(path: Path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'tools' in data:
        return data['tools'] or []
    return data if isinstance(data, list) else []


def _load_seed_file(path: Path):
    items = []
    if not path.exists():
        return items
    with path.open(encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception:
                continue
    return items


def _as_row(item: dict) -> dict:
    vid = item.get('vendor_id', '') or ''
    rid = item.get('id', '')
    return {
        'key': f"{rid}:{vid}",
        'id': rid,
        'vendor_id': vid,
        'router_value': item.get('router_value', 0.1) or 0.1,
        'tier': item.get('tier', 1) or 1,
        'category': item.get('category'),
        'popularity': item.get('adoption_prior'),
        'sentiment': item.get('sentiment_prior'),
    }


def build():
    rows = []
    seen = set()
    # primary source
    for obj in _load_tools_file(REGISTRY_TOOLS):
        rid = obj.get('id')
        if not rid or rid in seen:
            continue
        rows.append(_as_row(obj))
        seen.add(rid)
    # fallback to seed if needed
    if len(rows) < 50:
        for obj in _load_seed_file(REGISTRY_SEED):
            rid = obj.get('id')
            if not rid or rid in seen:
                continue
            rows.append(_as_row(obj))
            seen.add(rid)
            if len(rows) >= 50:
                break
    # sort
    rows.sort(key=lambda r: (-float(r.get('router_value', 0)), str(r.get('id', ''))))
    # write csv
    out_path = ARTIFACT_DIR / 'tools_canon.csv'
    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f'wrote {len(rows)} rows to {out_path}')
    return {"rows_canon": len(rows), "path": str(out_path)}


if __name__ == '__main__':
    metrics = build()
    # Emit JSON on the last line for automation hooks
    print(json.dumps(metrics))
