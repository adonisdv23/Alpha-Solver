import re
import csv
import json
import difflib
from pathlib import Path
from urllib.parse import urlparse

SOURCE_PATH = Path('docs/chatgpt-optimizer-final-3.md')
ARTIFACT_DIR = Path('artifacts')
ARTIFACT_DIR.mkdir(exist_ok=True)

COLUMNS = ["name", "category", "url", "description", "capabilities", "price", "tags", "notes"]

def slug(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip('-')
    return text

def parse():
    lines = SOURCE_PATH.read_text(encoding='utf-8').splitlines()
    entries = []
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('```'):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            if '|' in line:
                cells = [c.strip() for c in line.split('|')]
                if len(cells) >= len(COLUMNS):
                    entry = dict(zip(COLUMNS, cells[:len(COLUMNS)]))
                    entries.append(entry)
            i += 1
            continue
        if '|' in line and not line.lstrip().startswith('-'):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            if table_lines:
                headers = [h.strip().lower() for h in table_lines[0].strip().strip('|').split('|')]
                start = 1
                if len(table_lines) > 1 and set(table_lines[1].replace('|', '').strip()) <= set('-: '):
                    start = 2
                for row in table_lines[start:]:
                    cells = [c.strip() for c in row.strip().strip('|').split('|')]
                    if len(cells) != len(headers):
                        continue
                    entry = {headers[idx]: cells[idx] for idx in range(len(headers))}
                    entries.append(entry)
            continue
        m = re.match(r"-\s*(.+?)\s+—\s+(.*)\((https?://[^)]+)\)\s*(\[tags:\s*([^\]]+)\])?", line)
        if m:
            name = m.group(1).strip()
            desc = m.group(2).strip()
            url = m.group(3).strip()
            tags = m.group(5).split(',') if m.group(5) else []
            entry = {
                "name": name,
                "category": "",
                "url": url,
                "description": desc,
                "capabilities": "",
                "price": "",
                "tags": ",".join(t.strip() for t in tags),
                "notes": "",
            }
            entries.append(entry)
        i += 1
    return entries

def normalize(entry):
    norm = {c: "" for c in COLUMNS}
    for k, v in entry.items():
        key = k.lower()
        if key in norm:
            norm[key] = v
    url = norm.get('url', '')
    domain = urlparse(url).netloc if url else ''
    norm['url_domain'] = domain
    norm['id'] = f"{slug(norm.get('name', ''))}:{slug(domain)}" if domain else slug(norm.get('name', ''))
    return norm

def merge_entries(entries):
    canon = {}
    for e in entries:
        n = normalize(e)
        key = (n['name'].lower(), n['url_domain'])
        if key in canon:
            existing = canon[key]
            if len(n.get('description','')) > len(existing.get('description','')):
                existing['description'] = n['description']
            existing_tags = set(filter(None, existing.get('tags','').split(',')))
            new_tags = set(filter(None, n.get('tags','').split(',')))
            existing['tags'] = ','.join(sorted(existing_tags | new_tags))
            existing_caps = set(filter(None, existing.get('capabilities','').split(',')))
            new_caps = set(filter(None, n.get('capabilities','').split(',')))
            existing['capabilities'] = ','.join(sorted(existing_caps | new_caps))
            continue
        # check url dupes
        url = n.get('url')
        if url and any(c.get('url') == url for c in canon.values()):
            continue
        # fuzzy name within category
        for existing in canon.values():
            if existing.get('category') == n.get('category'):
                ratio = difflib.SequenceMatcher(None, existing.get('name','').lower(), n.get('name','').lower()).ratio()
                if ratio >= 0.9:
                    existing_tags = set(filter(None, existing.get('tags','').split(',')))
                    new_tags = set(filter(None, n.get('tags','').split(',')))
                    existing['tags'] = ','.join(sorted(existing_tags | new_tags))
                    existing_caps = set(filter(None, existing.get('capabilities','').split(',')))
                    new_caps = set(filter(None, n.get('capabilities','').split(',')))
                    existing['capabilities'] = ','.join(sorted(existing_caps | new_caps))
                    if len(n.get('description','')) > len(existing.get('description','')):
                        existing['description'] = n['description']
                    break
        else:
            canon[key] = n
    return list(canon.values())

def write_outputs(rows, parsed_count):
    csv_path = ARTIFACT_DIR / 'tools_canon.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS + ['url_domain', 'id'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    jsonl_path = ARTIFACT_DIR / 'tools_canon.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    catalog_path = ARTIFACT_DIR / 'tools_catalog.md'
    by_cat = {}
    for r in rows:
        cat = r.get('category') or 'uncategorized'
        by_cat.setdefault(cat, []).append(r)
    lines = []
    for cat, items in sorted(by_cat.items()):
        lines.append(f"## {cat} ({len(items)})")
        for it in sorted(items, key=lambda x: x.get('name','')):
            lines.append(f"- {it.get('name')}")
        lines.append('')
    top = sorted(rows, key=lambda r: len(' '.join([r.get('description',''), r.get('capabilities',''), r.get('notes','')])), reverse=True)[:25]
    lines.append('## Top 25 by evidence length')
    for it in top:
        lines.append(f"- {it.get('name')} ({len(' '.join([it.get('description',''), it.get('capabilities',''), it.get('notes','')]))})")
    catalog_path.write_text('\n'.join(lines), encoding='utf-8')
    quality_path = ARTIFACT_DIR / 'tools_quality.json'
    metrics = {
        'rows_parsed': parsed_count,
        'rows_canon': len(rows),
        'dupes_removed': parsed_count - len(rows),
        'coverage': (len(rows) / parsed_count) if parsed_count else 0,
    }
    quality_path.write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(json.dumps(metrics))

if __name__ == '__main__':
    parsed = parse()
    canon = merge_entries(parsed)
    write_outputs(canon, len(parsed))
