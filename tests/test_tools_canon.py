import csv
import subprocess
import sys
import unittest
from pathlib import Path

from alpha_solver_entry import AlphaSolver


class ToolsCanonTest(unittest.TestCase):
    def test_build_and_rank(self):
        subprocess.check_call([sys.executable, 'scripts/build_tools_canon.py'])
        csv_path = Path('artifacts/tools_canon.csv')
        self.assertTrue(csv_path.exists())
        with open(csv_path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 1)
        solver = AlphaSolver(tools_canon_path=str(csv_path))
        result = solver.solve('demo query')
        self.assertEqual(len(result['shortlist']), solver.k)
