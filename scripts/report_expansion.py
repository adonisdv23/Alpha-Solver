import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from alpha.core import loader

ARTIFACT_DIR = Path('artifacts')
ARTIFACT_DIR.mkdir(exist_ok=True)

registries_path = Path('registries')
clusters = loader.load_file(registries_path / 'clusters.yaml')
regions = loader.load_file(registries_path / 'regions.yaml')
patents = loader.load_file(registries_path / 'patents.yaml')
forecasts = loader.load_file(registries_path / 'forecasts.json')

lines = []
lines.append('# Expansion Report\n')
lines.append('## Cluster Map\n')
for cl in clusters.get('clusters', []):
    lines.append(f"- {cl.get('id')}: {len(cl.get('members', []))} members\n")
lines.append('\n## Region Matrix\n')
for r in regions.get('regions', []):
    allowed = ', '.join(r.get('allowed_vendors', []))
    lines.append(f"- {r.get('id')}: {allowed}\n")
lines.append('\n## Patent Docket\n')
for c in patents.get('candidates', []):
    claims = ', '.join(c.get('claims', []))
    lines.append(f"- {c.get('id')} ({c.get('status')}): {claims}\n")
lines.append('\n## Forecast Snapshot\n')
for f in forecasts.get('items', []):
    lines.append(f"- {f.get('id')}: {f.get('trend')} ({f.get('confidence')})\n")

(ARTIFACT_DIR / 'expansion_report.md').write_text(''.join(lines), encoding='utf-8')

metrics = {
    'clusters': len(clusters.get('clusters', [])),
    'regions': len(regions.get('regions', [])),
    'patents': len(patents.get('candidates', [])),
    'forecasts': len(forecasts.get('items', [])),
}
print(json.dumps(metrics))
