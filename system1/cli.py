#!/usr/bin/env python3
"""
System One & Third-Person Audit (TPA) Unified CLI
Commands:
  tpa status
  tpa test
  tpa audit --stage 1|2 --task "<task>" [--work "<current_work>"]
  tpa step --task "<task>" --step <N> --total <TOTAL> [--work "<current_work>"]
  tpa reset
"""

import sys
import os
import json
import argparse

from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion, get_client_config
from .tpa import tpa_step, run_tpa_audit, format_tpa_verdict_card, TPASessionLedger


def main():
    if len(sys.argv) < 2:
        print("System One: Third-Person Audit (TPA) Engine")
        print("Usage:")
        print("  tpa status                                            # Check active sessions & API provider")
        print("  tpa test                                              # Run live sub-100ms decision test")
        print("  tpa audit --stage 1|2 --task \"<task>\"                # Run on-demand 40% or 60% audit")
        print("  tpa step --task \"<task>\" --step <N> --total <TOTAL>   # Progress step (triggers at 40% & 60%)")
        print("  tpa reset                                             # Reset local session ledger")
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

    elif cmd == "reset":
        all_data = TPASessionLedger.load_all()
        for sid in list(all_data.keys()):
            TPASessionLedger.reset_session(sid)
        print("All TPA session ledgers have been reset.")

    elif cmd == "audit":
        parser = argparse.ArgumentParser(prog="tpa audit")
        parser.add_argument("--stage", type=int, default=1, choices=[1, 2], help="1=Mid-flight bias (40%), 2=Convergence (60%)")
        parser.add_argument("--task", type=str, required=True, help="Task description")
        parser.add_argument("--work", type=str, default="Current state", help="Summary of work or tests done")
        parser.add_argument("--directives", type=str, default="", help="Human directives or assumptions")
        args = parser.parse_args(sys.argv[2:])

        verdict = run_tpa_audit(args.task, stage=args.stage, current_work=args.work, human_directives=args.directives)
        card = format_tpa_verdict_card(verdict, args.task, 45.0 if args.stage == 1 else 65.0)
        print(card)

    elif cmd == "step":
        parser = argparse.ArgumentParser(prog="tpa step")
        parser.add_argument("--task", type=str, required=True, help="Task description")
        parser.add_argument("--step", type=int, required=True, help="Current step number")
        parser.add_argument("--total", type=int, default=10, help="Total planned steps")
        parser.add_argument("--work", type=str, default="", help="Summary of work done in this step")
        args = parser.parse_args(sys.argv[2:])

        res = tpa_step(args.task, current_step=args.step, total_steps=args.total, step_summary=args.work)
        if res["triggered"]:
            print(res["verdict_card"])
        else:
            print(f"TPA Step {args.step}/{args.total} recorded ({res['progress_pct']:.1f}%). Watermark not triggered.")

    else:
        print(f"Unknown command: {cmd}. Run 'tpa' for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
