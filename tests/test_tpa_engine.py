import unittest
from system1.tpa import tpa_step, TPASessionLedger, format_tpa_verdict_card

class TestTPAEngine(unittest.TestCase):
    def setUp(self):
        self.task = "Unit test synthetic task for TPA watermark verification"
        self.session_id = "test_session_tpa_unit"
        TPASessionLedger.reset_session(self.session_id)

    def tearDown(self):
        TPASessionLedger.reset_session(self.session_id)

    def test_below_watermark_no_trigger(self):
        # 20% progress should not trigger any stage
        res = tpa_step(
            self.task,
            current_step=2,
            total_steps=10,
            progress_pct=20.0,
            session_id=self.session_id
        )
        self.assertFalse(res["triggered"])
        self.assertIsNone(res["stage"])

    def test_stage1_watermark_trigger_and_latch(self):
        # 45% progress crosses 40% threshold -> Stage 1 triggers
        res = tpa_step(
            self.task,
            current_step=4,
            total_steps=10,
            progress_pct=45.0,
            session_id=self.session_id
        )
        self.assertTrue(res["triggered"])
        self.assertEqual(res["stage"], 1)

        # Immediate follow-up at 48% must be latched (no repeat)
        res_repeat = tpa_step(
            self.task,
            current_step=5,
            total_steps=10,
            progress_pct=48.0,
            session_id=self.session_id
        )
        self.assertFalse(res_repeat["triggered"])

    def test_stage2_watermark_trigger_and_latch(self):
        # Manually latch stage 1 first
        TPASessionLedger.update_session(self.session_id, {"stage1_latched": True})

        # 65% progress crosses 60% threshold -> Stage 2 triggers
        res = tpa_step(
            self.task,
            current_step=6,
            total_steps=10,
            progress_pct=65.0,
            session_id=self.session_id
        )
        self.assertTrue(res["triggered"])
        self.assertEqual(res["stage"], 2)

        # Immediate follow-up at 70% must be latched
        res_repeat = tpa_step(
            self.task,
            current_step=7,
            total_steps=10,
            progress_pct=70.0,
            session_id=self.session_id
        )
        self.assertFalse(res_repeat["triggered"])

    def test_verdict_card_formatting(self):
        mock_verdict = {
            "stage": 1,
            "checkpoint_band": "40% - 50%",
            "status": "HALT & RESTRUCTURE",
            "requires_halt": True,
            "detected_pattern": "missing_prerequisites",
            "confidence": 0.95,
            "alignment_score": 0.85,
            "one_question_that_unlocks_everything": "verify_root_deliverable"
        }
        card = format_tpa_verdict_card(mock_verdict, "Test task description", 45.0)
        self.assertIn("THIRD-PERSON AUDIT (TPA)", card)
        self.assertIn("HALT & RESTRUCTURE", card)
        self.assertIn("The One Unlock Question", card)

if __name__ == "__main__":
    unittest.main()
