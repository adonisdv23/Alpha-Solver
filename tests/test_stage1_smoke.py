import unittest

from alpha_solver_entry import AlphaSolver


class Stage1SmokeTest(unittest.TestCase):
    def test_response_keys(self):
        solver = AlphaSolver()
        result = solver.solve('demo query')
        required = [
            'pending_questions',
            'shortlist',
            'orchestration_plan',
            'solution',
            'confidence',
            'response_time_ms',
            'telemetry_contract',
            'expert_team',
            'eligibility_analysis',
            'requirements_analysis',
            'safe_out_state',
        ]
        for key in required:
            self.assertIn(key, result)


if __name__ == '__main__':
    unittest.main()
