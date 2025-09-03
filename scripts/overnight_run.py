#!/usr/bin/env python3
"""Overnight pipeline for Alpha Solver"""
import json
import subprocess
import runpy
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
import zipfile

parser = argparse.ArgumentParser(description="Alpha Solver overnight pipeline")
parser.add_argument("--regions", default="EU,''", help="comma-separated regions; '' means no-region")
parser.add_argument("--k", type=int, default=5, help="top-N tools")
parser.add_argument("--queries", default="", help="path to queries file")
args = parser.parse_args()

ART_DIR = Path('artifacts')
ART_DIR.mkdir(exist_ok=True)

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

regions: list[str] = []
for r in args.regions.split(','):
    r = r.strip()
    if r in ("", "''", '""'):
        regions.append("")
    else:
        regions.append(r)

if args.queries and Path(args.queries).is_file():
    queries = [line.strip() for line in Path(args.queries).read_text(encoding='utf-8').splitlines() if line.strip()]
else:
    queries = [
        "legal contract review",
        "edge deployment",
        "security posture",
        "healthcare triage",
        "enterprise SaaS integration",
    ]

summary = {
    "timestamp": datetime.utcnow().isoformat(),
    "preflight": {},
    "canon_metrics": {},
    "runs": {},
    "report": {},
    "tests": "FAIL",
    "files": []
}

def log(msg):
    print(msg)

def run_json(cmd):
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = proc.stdout.strip().splitlines()
        return json.loads(lines[-1]) if lines else {}
    except Exception as e:
        log(f"ERROR: {' '.join(cmd)} -> {e}")
        return {"error": str(e)}

# Step A
log("Step A: preflight")
summary['preflight'] = run_json([sys.executable, 'scripts/preflight.py'])

# Step B
log("Step B: build tools canon")
summary['canon_metrics'] = run_json([sys.executable, 'scripts/build_tools_canon.py'])
if summary['canon_metrics'].get('rows_canon', 0) < 50:
    log("WARNING: tools canon has fewer than 50 rows")

# Step C
log("Step C: solver sweeps")
ns = runpy.run_path('Alpha Solver.py', run_name='alpha_solver_module')
AlphaSolver = ns['AlphaSolver']
leaderboard = {}

def run_solver(region: str):
    solver = AlphaSolver(tools_canon_path='artifacts/tools_canon.csv',
                         registries_path='registries',
                         k=args.k, deterministic=True, region=region)
    runs = []
    for q in queries:
        start = time.time()
        try:
            res = solver.solve(q)
            elapsed = res.get('response_time_ms')
            pq_counts = {k: len(v) for k, v in res.get('pending_questions', {}).items()}
            steps = len(res.get('orchestration_plan', {}).get('steps', []))
            runs.append({
                "query": q,
                "shortlist": [{"id": t.get('id'), "score": t.get('score')} for t in res.get('shortlist', [])],
                "pending_questions": pq_counts,
                "plan_steps": steps,
                "time_ms": elapsed
            })
            for t in res.get('shortlist', []):
                tid = t.get('id')
                if not tid:
                    continue
                score = t.get('score') or 0
                name = t.get('name', '')
                cur = leaderboard.get(tid)
                if cur is None or score > cur['score']:
                    leaderboard[tid] = {"id": tid, "name": name, "score": score}
        except Exception as e:
            log(f"ERROR solving '{q}' for region '{region}': {e}")
            runs.append({
                "query": q,
                "shortlist": [],
                "pending_questions": {},
                "plan_steps": 0,
                "time_ms": None,
                "error": str(e)
            })
    return runs

run_matrix = {}
for region in regions:
    label = region if region else 'none'
    run_matrix[label] = {"queries": run_solver(region)}
    summary['runs'][label] = run_matrix[label]
    (ART_DIR / f'run_{label}.json').write_text(json.dumps(run_matrix[label], indent=2), encoding='utf-8')
(ART_DIR / 'run_matrix.json').write_text(json.dumps(run_matrix, indent=2), encoding='utf-8')

# Step D
log("Step D: expansion report")
summary['report'] = run_json([sys.executable, 'scripts/report_expansion.py'])

# Step E
log("Step E: tests")
try:
    proc = subprocess.run([sys.executable, '-m', 'unittest', '-q'], text=True, capture_output=True)
    summary['tests'] = 'PASS' if proc.returncode == 0 else 'FAIL'
    if proc.returncode != 0:
        log(proc.stdout + proc.stderr)
except Exception as e:
    summary['tests'] = 'FAIL'
    log(f"ERROR running tests: {e}")

# Step F
log("Step F: leaderboard")
items = list(leaderboard.values())
items.sort(key=lambda x: (-x['score'], x['name']))
lines = ['# Leaderboard\n']
for i, t in enumerate(items[:15], 1):
    lines.append(f"{i}. {t['name']} ({t['id']}) - {t['score']:.2f}\n")
(ART_DIR / 'leaderboard.md').write_text(''.join(lines), encoding='utf-8')

# Step G
summary_path = ART_DIR / 'overnight_summary.json'
with summary_path.open('w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)
files = [str(p) for p in sorted(ART_DIR.glob('*')) if p.is_file() and p.name != 'overnight_bundle.zip']
summary['files'] = files
with summary_path.open('w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

# Step H
log("Step H: bundle artifacts")
bundle_path = ART_DIR / 'overnight_bundle.zip'
with zipfile.ZipFile(bundle_path, 'w') as zf:
    for p in ART_DIR.iterdir():
        if p.is_file() and p.name != 'overnight_bundle.zip':
            zf.write(p, p.name)

print(json.dumps({"ok": True, "regions": len(regions), "k": args.k, "queries": len(queries)}))
