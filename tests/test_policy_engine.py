import unittest
from alpha.core import loader
from alpha.core.policy import PolicyEngine

class PolicyEngineTest(unittest.TestCase):
    def test_policy_checks(self):
        regs = loader.load_all('registries')
        pe = PolicyEngine(regs)
        ctx = {"vendor_id": "demo.vendor", "cost_estimate": 0.5, "data_tags": ["phi"], "op": "test"}
        budget = pe.check_budget(ctx)
        self.assertIn('ok', budget)
        self.assertIn('action', budget)
        dc = pe.classify(["phi"])
        self.assertTrue(dc.get('masked') or dc.get('notes'))
        cb = pe.circuit_guard("demo.vendor")
        self.assertIn('state', cb)
        self.assertIn('allow', cb)

if __name__ == '__main__':
    unittest.main()
