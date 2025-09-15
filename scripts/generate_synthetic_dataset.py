import argparse
import json
from pathlib import Path
import random


def write_jsonl(path: Path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for obj in sorted(items, key=lambda x: x['id']):
            f.write(json.dumps(obj, sort_keys=True) + '\n')


def generate_pii(path: Path):
    items = []
    for i in range(1, 51):
        items.append({
            'id': i,
            'text': f"Reach me at user{i}@example.com",
            'label': 'email'
        })
    for i in range(51, 101):
        items.append({
            'id': i,
            'text': f"My number is 555-010{i:03d}",
            'label': 'phone'
        })
    write_jsonl(path, items)


def generate_routing(path: Path):
    items = []
    for i in range(1, 16):
        items.append({
            'id': i,
            'query': f"What is {i} plus {i}?",
            'label': 'llm_only'
        })
    for i in range(16, 31):
        items.append({
            'id': i,
            'query': f"Use the database tool to fetch record {i}",
            'label': 'mcp'
        })
    write_jsonl(path, items)


def generate_replay(path: Path):
    items = []
    seed = 1234
    for i in range(1, 11):
        rnd = random.Random(seed + i)
        items.append({
            'id': i,
            'input': f"event {i}",
            'result': rnd.randint(0, 1000)
        })
    write_jsonl(path, items)


def main(root: Path):
    generate_pii(root / 'pii/labels_email_phone.jsonl')
    generate_routing(root / 'routing/scenarios_routing.jsonl')
    generate_replay(root / 'replay/replay_small.jsonl')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-root', default=Path(__file__).resolve().parent.parent / 'data/datasets')
    args = parser.parse_args()
    main(Path(args.output_root))
