"""Loader for canonical tools dataset"""
import csv
import json
from pathlib import Path
from typing import List, Dict

def load_tools_canon(path: str) -> List[Dict]:
    p = Path(path)
    tools: List[Dict] = []
    if p.suffix.lower() == '.csv':
        with open(p, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tools.append(row)
    elif p.suffix.lower() == '.jsonl':
        with open(p, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    tools.append(json.loads(line))
    else:
        raise ValueError('Unsupported tools canon format')
    tools.sort(key=lambda t: (-float(t.get('router_value', 0) or 0), t.get('name', '')))
    return tools
