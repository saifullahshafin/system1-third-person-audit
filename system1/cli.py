#!/usr/bin/env python3
"""
System One & Third-Person Audit (TPA) Master CLI
Author: Saifullah Shafin
Usage:
  system1 status                                  # Check active provider & sessions
  system1 test                                    # Run sub-100ms decision test
  system1 route "<task_description>"              # Route task to subsystem & risk tier
  system1 audit-code "<diff_or_file>"             # Audit code diff for security defects
  system1 video-eval "<transcript_or_file>"       # Evaluate content signal-to-noise
  system1 tpa audit --stage 1|2 --task "<task>"   # Run Third-Person Audit
  system1 tpa step --task "<task>" --step <N>     # Progress step with watermark trigger
  system1 mcp                                     # Start Model Context Protocol server
  system1 reset                                   # Reset session ledger
"""

import sys
import os
import json
import argparse

from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion, get_client_config
from .tpa import tpa_step, run_tpa_audit, format_tpa_verdict_card, TPASessionLedger
from .security import audit_code
from .router import route_task
from .evaluator import evaluate_video_transcript
from .mcp_server import run_stdio_server


def main():
    if len(sys.argv) < 2:
        print("System One: Master Deterministic Decision Architecture & Third-Person Audit (TPA)")
        print("Lead System Architect: Saifullah Shafin\n")
        print("Commands:")
        print("  system1 status                                  # Check active provider & sessions")
        print("  system1 test                                    # Run live sub-100ms decision test")
        print("  system1 route \"<task_description>\"              # Route task to subsystem & security risk tier")
        print("  system1 audit-code \"<diff_or_file>\"             # Audit code diff for security defects & drift")
        print("  system1 video-eval \"<transcript_or_file>\"       # Evaluate video transcript in 80ms")
        print("  system1 tpa audit --stage 1|2 --task \"<task>\"   # Run on-demand Third-Person Audit (40% or 60%)")
        print("  system1 tpa step --task \"<task>\" --step <N>     # Progress step (triggers at 40% & 60%)")
        print("  system1 mcp                                     # Start Model Context Protocol stdio server")
        print("  system1 reset                                   # Reset session ledger")
        print("\nEnvironment variables:")
        print("  TYPESAFE_API_KEY      Official TypeSafe API ($5 free credit)")
        print("  OPENROUTER_API_KEY    OpenRouter Decisions fallback")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        cfg = get_client_config()
        print("System One Client Configuration:")
        print(f"  Active Provider:    {cfg['provider']}")
        print(f"  Endpoint:           {cfg['url']}")
        print(f"  Key Detected:       {'Yes' if cfg['key'] else 'No'}")
        print(f"  Default Model:      {cfg['model']}")

        sessions = TPASessionLedger.load_all()
        print(f"\nActive TPA Sessions:  {len(sessions)}")
        for sid, s in sessions.items():
            print(f"  [{sid}] Progress: {s.get('progress_pct', 0.0):.1f}% | Stage 1: {s.get('stage1_latched')} | Stage 2: {s.get('stage2_latched')}")

    elif cmd == "test":
        cfg = get_client_config()
        if not cfg["key"]:
            print("[Error] Neither TYPESAFE_API_KEY nor OPENROUTER_API_KEY detected.")
            print("Set your key in .env or environment to proceed.")
            sys.exit(1)

        print(f"Testing System One decision latency via {cfg['provider']} ({cfg['model']})...")
        sample_state = "Production checkout database replica lagged by 45 seconds during flash sale."
        sample_questions = {
            "urgency": ScoreQuestion("How urgent is this incident?", ["low", "moderate", "critical"]),
            "is_outage": NoulQuestion("Is this an active customer outage?")
        }
        try:
            res = evaluate_state(sample_state, sample_questions)
            print("\nResponse Received Successfully in sub-100ms:")
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"Execution Error: {e}")
            sys.exit(1)

    elif cmd == "route":
        if len(sys.argv) < 3:
            print("Usage: system1 route \"<task_description>\"")
            sys.exit(1)
        task_desc = sys.argv[2]
        res = route_task(task_desc)
        print("System One Task Routing Result:")
        print(f"  Target Subsystem:         {res['intent']} (Conf: {res['confidence']*100:.1f}%)")
        print(f"  Security Risk Tier:       {res['risk_tier']:.2f} / 2.0")
        print(f"  Requires Human Approval:  {res['requires_human_approval']}")

    elif cmd == "audit-code":
        if len(sys.argv) < 3:
            print("Usage: system1 audit-code \"<diff_or_file>\"")
            sys.exit(1)
        target = sys.argv[2]
        content = target
        if os.path.exists(target):
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        res = audit_code(content)
        print("System One Code Safety Audit Result:")
        print(f"  Status:                   {res['status']}")
        print(f"  Risk Category:            {res['risk_category']} (Conf: {res['confidence']*100:.1f}%)")
        print(f"  Risk Tier Score:          {res['risk_tier_score']:.2f} / 2.0")
        print(f"  Blocked:                  {res['is_blocked']}")
        print(f"  Requires Human Approval:  {res['requires_human_approval']}")

    elif cmd == "video-eval":
        if len(sys.argv) < 3:
            print("Usage: system1 video-eval \"<transcript_or_file>\"")
            sys.exit(1)
        target = sys.argv[2]
        content = target
        if os.path.exists(target):
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        res = evaluate_video_transcript(content)
        print("System One Content Signal Evaluation Result:")
        print(f"  Signal-to-Noise Score:    {res['signal_score']:.2f} / 2.0 (High Signal: {res['is_high_signal']})")
        print(f"  Content Pillar:           {res['content_pillar']}")
        print(f"  Monetizable Opportunity:  {res['is_monetizable']}")

    elif cmd in ("tpa", "hmo"):
        sub_args = sys.argv[2:]
        if not sub_args or sub_args[0] == "audit":
            parser = argparse.ArgumentParser(prog="system1 tpa audit")
            parser.add_argument("--stage", type=int, default=1, choices=[1, 2], help="1=Mid-flight bias (40%), 2=Convergence (60%)")
            parser.add_argument("--task", type=str, required=True, help="Task description")
            parser.add_argument("--work", type=str, default="Current state", help="Summary of work or tests done")
            parser.add_argument("--directives", type=str, default="", help="Human directives or assumptions")
            parsed = parser.parse_args(sub_args[1:] if sub_args and sub_args[0] == "audit" else sub_args)

            verdict = run_tpa_audit(parsed.task, stage=parsed.stage, current_work=parsed.work, human_directives=parsed.directives)
            card = format_tpa_verdict_card(verdict, parsed.task, 45.0 if parsed.stage == 1 else 65.0)
            print(card)
        elif sub_args[0] == "step":
            parser = argparse.ArgumentParser(prog="system1 tpa step")
            parser.add_argument("--task", type=str, required=True, help="Task description")
            parser.add_argument("--step", type=int, required=True, help="Current step number")
            parser.add_argument("--total", type=int, default=10, help="Total planned steps")
            parser.add_argument("--work", type=str, default="", help="Summary of work done in this step")
            parsed = parser.parse_args(sub_args[1:])

            res = tpa_step(parsed.task, current_step=parsed.step, total_steps=parsed.total, step_summary=parsed.work)
            if res["triggered"]:
                print(res["verdict_card"])
            else:
                print(f"TPA Step {parsed.step}/{parsed.total} recorded ({res['progress_pct']:.1f}%). Watermark not triggered.")
        elif sub_args[0] == "reset":
            all_data = TPASessionLedger.load_all()
            for sid in list(all_data.keys()):
                TPASessionLedger.reset_session(sid)
            print("All TPA session ledgers have been reset.")
        else:
            print(f"Unknown TPA subcommand: {sub_args[0]}")

    elif cmd == "mcp":
        run_stdio_server()

    elif cmd == "reset":
        all_data = TPASessionLedger.load_all()
        for sid in list(all_data.keys()):
            TPASessionLedger.reset_session(sid)
        print("All TPA session ledgers have been reset.")

    # Direct tpa alias fallback
    elif cmd == "audit":
        sys.argv = [sys.argv[0], "tpa", "audit"] + sys.argv[2:]
        main()

    elif cmd == "step":
        sys.argv = [sys.argv[0], "tpa", "step"] + sys.argv[2:]
        main()

    else:
        print(f"Unknown command: {cmd}. Run 'system1' for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
