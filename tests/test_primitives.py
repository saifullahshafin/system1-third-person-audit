import unittest
from system1.bridge import ChoiceQuestion, ScoreQuestion, NoulQuestion, get_client_config

class TestSystemOnePrimitives(unittest.TestCase):
    def test_choice_question_structure(self):
        q = ChoiceQuestion(
            instructions="Select primary color scheme",
            criteria={"dark": "Dark mode palette", "light": "Light mode palette"}
        )
        self.assertEqual(q["type"], "choice")
        self.assertEqual(q["instructions"], "Select primary color scheme")
        self.assertIn("dark", q["criteria"])
        self.assertIn("light", q["criteria"])

    def test_score_question_structure(self):
        q = ScoreQuestion(
            instructions="Rate urgency level",
            criteria=["Low priority", "Medium priority", "Critical priority"]
        )
        self.assertEqual(q["type"], "score")
        self.assertEqual(len(q["criteria"]), 3)

    def test_noul_question_structure(self):
        q = NoulQuestion(instructions="Is system healthy?")
        self.assertEqual(q["type"], "noul")
        self.assertEqual(q["instructions"], "Is system healthy?")

    def test_client_config_detection(self):
        cfg = get_client_config()
        self.assertIn("provider", cfg)
        self.assertIn("url", cfg)
        self.assertIn("model", cfg)

if __name__ == "__main__":
    unittest.main()
