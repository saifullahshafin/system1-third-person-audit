#!/usr/bin/env python3
"""
System One & Third-Person Audit (TPA) Interactive Demo
Demonstrates how an autonomous agent loop automatically triggers TPA audits
at the 40% mid-flight watermark and 60% convergence watermark.
"""

import sys
import time
from system1.tpa import tpa_step, TPASessionLedger

SAMPLE_TASK = "Refactor customer billing pipeline to support dynamic multi-tier usage pricing"

STEPS = [
    (1, 10, "Inspected current Stripe invoice sync controller"),
    (2, 20, "Identified bottleneck in batch processing query"),
    (3, 30, "Created draft database schema for usage tiers"),
    (4, 45, "Drafted pricing calculator skipping edge cases around pro-rated billing"),  # Crosses 40% watermark!
    (5, 50, "Added preliminary controller endpoints"),
    (6, 65, "Implemented billing service without retry queues or webhook idempotency"), # Crosses 60% watermark!
    (7, 75, "Added integration test skeleton"),
    (8, 85, "Configured environment variables and documentation"),
    (9, 95, "Ran test suite and verified endpoints"),
    (10, 100, "Cleaned up code and prepared git commit")
]


def run_demo():
    print("================================================================================")
    print("SYSTEM ONE: THIRD-PERSON AUDIT (TPA) INTERACTIVE RUNTIME DEMO")
    print("================================================================================")
    print(f"Task: {SAMPLE_TASK}\n")
    print("Simulating an agent executing a 10-step deep building workflow...")
    print("Watch the dual watermark checkpoints (40% and 60%) trigger automatically.\n")

    session_id = "demo_tpa_session"
    TPASessionLedger.reset_session(session_id)

    for step_num, pct, summary in STEPS:
        print(f"--> [Step {step_num:02d}/10] ({pct:3.0f}%) {summary}")
        time.sleep(0.3)

        # One-line agent hook call
        res = tpa_step(
            task=SAMPLE_TASK,
            current_step=step_num,
            total_steps=10,
            progress_pct=float(pct),
            step_summary=summary,
            session_id=session_id
        )

        if res["triggered"]:
            print("\n*** WATERMARK CROSSED: THIRD-PERSON AUDIT TRIGGERED ***")
            print(res["verdict_card"])
            print("--------------------------------------------------------------------------------\n")
            time.sleep(0.5)

    TPASessionLedger.reset_session(session_id)
    print("================================================================================")
    print("DEMO COMPLETE: Two audits triggered automatically; zero manual polling required.")
    print("================================================================================\n")


if __name__ == "__main__":
    run_demo()
