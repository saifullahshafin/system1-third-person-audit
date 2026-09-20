import unittest
from system1.evaluator import evaluate_video_transcript

class TestEvaluator(unittest.TestCase):
    def test_transcript_evaluation(self):
        sample = "In this video, I break down the exact high-ticket B2B sales playbook that scaled our agency from zero to $50k MRR."
        res = evaluate_video_transcript(sample, title="Agency Scaling Blueprint")
        self.assertIn("signal_score", res)
        self.assertIn("content_pillar", res)
        self.assertIn("is_monetizable", res)

if __name__ == "__main__":
    unittest.main()
