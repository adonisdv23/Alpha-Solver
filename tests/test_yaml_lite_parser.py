import unittest, json
from pathlib import Path
import runpy

ns = runpy.run_path('alpha/core/loader.py')
load_file = ns['load_file']

class YamlLiteTest(unittest.TestCase):
    def test_regions(self):
        data = load_file(Path('registries/regions.yaml'))
        self.assertTrue(data.get('regions'), 'regions should not be empty')
    def test_clusters(self):
        data = load_file(Path('registries/clusters.yaml'))
        self.assertTrue(data.get('clusters'), 'clusters should not be empty')
    def test_patents(self):
        data = load_file(Path('registries/patents.yaml'))
        self.assertTrue(data.get('candidates'), 'patents should not be empty')

if __name__ == '__main__':
    unittest.main()
