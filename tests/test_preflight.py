import json
import subprocess
import sys
from pathlib import Path
import unittest

class PreflightTest(unittest.TestCase):
    def test_preflight_ok(self):
        proc = subprocess.run([sys.executable, 'scripts/preflight.py'], capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout.strip())
        self.assertTrue(data.get('ok'))

if __name__ == '__main__':
    unittest.main()
