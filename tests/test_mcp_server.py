import unittest
from system1.mcp_server import create_tools_manifest, handle_tool_call

class TestTPAMCPServer(unittest.TestCase):
    def test_manifest_tools(self):
        manifest = create_tools_manifest()
        tool_names = [t["name"] for t in manifest]
        self.assertIn("system1_choice", tool_names)
        self.assertIn("system1_score", tool_names)
        self.assertIn("system1_noul", tool_names)
        self.assertIn("system1_tpa_step", tool_names)
        self.assertIn("system1_third_person_audit", tool_names)
        self.assertIn("system1_task_route", tool_names)

    def test_handle_tpa_step_call(self):
        res = handle_tool_call("system1_tpa_step", {
            "task": "Test unit MCP task",
            "current_step": 1,
            "total_steps": 10,
            "progress_pct": 10.0
        })
        self.assertIn("content", res)
        self.assertEqual(res["content"][0]["type"], "text")

if __name__ == "__main__":
    unittest.main()
