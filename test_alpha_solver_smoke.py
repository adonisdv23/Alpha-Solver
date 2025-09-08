import json
from pathlib import Path

from alpha_solver_entry import AlphaSolver

solver = AlphaSolver()

queries = ['simple', 'complex reasoning needed', '']
report = []
success = True

for q in queries:
    try:
        res = solver.solve(q)
        required = ['solution', 'confidence', 'response_time_ms', 'telemetry_contract',
                    'expert_team', 'eligibility_analysis', 'requirements_analysis', 'safe_out_state']
        assert all(k in res for k in required)
        if 'accessibility' in res:
            assert 'score' in res['accessibility']
        report.append({'query': q, 'ok': True})
    except Exception as e:  # pragma: no cover - diagnostic script
        success = False
        report.append({'query': q, 'ok': False, 'error': str(e)})

log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
with open(log_dir / 'smoke_results.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print('SMOKE TEST', 'PASS' if success else 'FAIL')
