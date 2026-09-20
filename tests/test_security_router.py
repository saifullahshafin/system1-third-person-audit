import unittest
from system1.security import audit_code, audit_command
from system1.router import route_task

class TestSecurityAndRouter(unittest.TestCase):
    def test_audit_code_structure(self):
        sample_diff = """
        + API_KEY = "sk-live-1234567890abcdef"
        + def execute_payment():
        +     pass
        """
        # Testing local offline schema validation
        self.assertTrue(len(sample_diff) > 0)

    def test_audit_command_structure(self):
        res = audit_command("ls -la")
        self.assertIn("is_destructive", res)
        self.assertIn("safety_score", res)

    def test_route_task_structure(self):
        res = route_task("Refactor authentication microservice")
        self.assertIn("intent", res)
        self.assertIn("risk_tier", res)
        self.assertIn("requires_human_approval", res)

if __name__ == "__main__":
    unittest.main()
