#!/usr/bin/env python3
"""
Example 2: Integrating Third-Person Audit into an Autonomous Agent Loop
Demonstrates how to plug `tpa_step` into any LangChain, AutoGen, CrewAI,
or custom Python agent runtime with zero boilerplate.
"""

from system1.tpa import tpa_step

def run_my_agent_loop(task: str, total_milestones: int):
    print(f"Starting agent execution: '{task}'")

    for step in range(1, total_milestones + 1):
        # 1. Agent executes mechanical work...
        summary = f"Completed sub-task milestone {step} of {total_milestones}"

        # 2. Hook into Third-Person Audit
        audit = tpa_step(
            task=task,
            current_step=step,
            total_steps=total_milestones,
            step_summary=summary
        )

        # 3. If a watermark threshold triggered, check status
        if audit["triggered"]:
            print(f"\n[TPA ALERT] Watermark reached on step {step} ({audit['progress_pct']:.1f}%)")
            print(audit["verdict_card"])

            if audit["requires_halt"]:
                print("\n[HALT] Critical bias or drift detected. Pausing agent for human alignment.")
                # Break or await human input
                break

    print("Agent loop concluded.")

if __name__ == "__main__":
    run_my_agent_loop("Migrate customer auth to WebAuthn passkeys", total_milestones=10)
