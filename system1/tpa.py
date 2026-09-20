#!/usr/bin/env python3
"""
Third-Person Audit (TPA) Engine
Author: Saifullah Shafin (Lead System Architect)
Subsystem: System One (TypeSafe Jev) Decision Protocol

Core Concept:
Steps COMPLETELY OUTSIDE the agent execution tunnel during deep work sessions to detect:
1. Mutual Human-Agent Cognitive Bias & Echo Chambers ("Yes-man" agreement loops).
2. Objective Drift (XY Problems) and Premature Optimization.
3. False 100% Completion (50% execution disguised as 100% production-ready).

Dual-Stage Watermark Checkpoints:
- Stage 1 (40% - 50% Progress): Mid-Flight Sanity & Bias Interception
- Stage 2 (60% - 70% Progress): Deep Convergence & False Completion Audit
"""

import os
import sys
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Union

from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion

# Local session state ledger
LEDGER_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_LEDGER_FILE = os.path.join(LEDGER_DIR, "tpa_session_state.json")


def _get_task_hash(task: str, workspace: Optional[str] = None) -> str:
    seed = f"{task.strip().lower()}_{workspace or ''}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]


class TPASessionLedger:
    """Thread-safe persistent ledger tracking task progress and watermark latches."""

    @staticmethod
    def load_all() -> Dict[str, Any]:
        if not os.path.exists(STATE_LEDGER_FILE):
            return {}
        try:
            with open(STATE_LEDGER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def save_all(data: Dict[str, Any]) -> None:
        try:
            with open(STATE_LEDGER_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            sys.stderr.write(f"[TPA Warning] Failed to persist session ledger: {e}\n")

    @classmethod
    def get_session(cls, session_id: str) -> Dict[str, Any]:
        all_data = cls.load_all()
        if session_id not in all_data:
            all_data[session_id] = {
                "session_id": session_id,
                "created_at": time.time(),
                "updated_at": time.time(),
                "progress_pct": 0.0,
                "current_step": 0,
                "total_steps": 10,
                "stage1_latched": False,
                "stage2_latched": False,
                "stage1_verdict": None,
                "stage2_verdict": None,
                "audit_history": []
            }
            cls.save_all(all_data)
        return all_data[session_id]

    @classmethod
    def update_session(cls, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        all_data = cls.load_all()
        session = all_data.get(session_id, {
            "session_id": session_id,
            "created_at": time.time(),
            "stage1_latched": False,
            "stage2_latched": False,
            "audit_history": []
        })
        session.update(updates)
        session["updated_at"] = time.time()
        all_data[session_id] = session
        cls.save_all(all_data)
        return session

    @classmethod
    def reset_session(cls, session_id: str) -> None:
        all_data = cls.load_all()
        if session_id in all_data:
            del all_data[session_id]
            cls.save_all(all_data)


# ----------------------------------------------------------------------
# Core Audit Diagnostic Engines (System One Gated)
# ----------------------------------------------------------------------

def run_stage1_midflight_audit(
    task_context: str,
    current_work: str,
    human_directives: Optional[str] = None,
    workspace: Optional[str] = None
) -> Dict[str, Any]:
    """
    STAGE 1: 40% - 50% MID-FLIGHT SANITY & BIAS INTERCEPTION
    Steps completely outside the execution tunnel from a third-person perspective.
    """
    state_payload = {
        "original_task": task_context,
        "current_implementation_state": current_work,
        "human_directives_or_assumptions": human_directives or "None provided",
        "workspace": workspace or "Default"
    }

    questions = {
        "holistic_bias_pattern": ChoiceQuestion(
            instructions=(
                "Step COMPLETELY OUTSIDE the current execution tunnel. From a third-person meta-observer "
                "perspective, audit the original task, current work, and human directives. "
                "What is the most dangerous hidden bias, assumption, or flaw currently at play?"
            ),
            criteria={
                "human_agent_echo_chamber": (
                    "The agent uncritically accepted a biased, flawed, or suboptimal premise from the human "
                    "without technical verification, creating an echo-chamber of false certainty."
                ),
                "objective_drift": (
                    "The work has drifted into an adjacent problem (XY problem) rather than solving "
                    "the true root goal."
                ),
                "missing_prerequisites": (
                    "The current work is building on quicksand: critical assets, schemas, dependencies, "
                    "or requirements have not been established yet."
                ),
                "premature_overengineering": (
                    "The agent is creating excessive abstractions, unnecessary subsystems, or bloated "
                    "architecture for what was a direct mechanical or focused task."
                ),
                "sound_and_aligned": (
                    "The approach is objectively sound. The work is directly solving the true root problem "
                    "with zero detected bias or drift."
                )
            }
        ),
        "is_direction_fundamentally_sound": NoulQuestion(
            instructions=(
                "Is the agent solving the TRUE root problem from first principles — or efficiently solving "
                "the wrong problem? True = fundamentally sound and unbiased."
            )
        ),
        "one_question_that_unlocks_everything": ChoiceQuestion(
            instructions=(
                "If only ONE question could be asked to break the illusion, expose hidden assumptions, "
                "or re-align the work before heavy sunk cost accumulates, what is it?"
            ),
            criteria={
                "verify_root_deliverable": (
                    "What is the exact, verifiable deliverable that constitutes 100% success for this task?"
                ),
                "verify_underlying_premise": (
                    "Is the core premise or hypothesis behind this approach actually true, or an unverified assumption?"
                ),
                "verify_prerequisite_assets": (
                    "Do the essential foundation files, data, and access exist right now to build this correctly?"
                ),
                "verify_simplest_path": (
                    "Can this be solved with a 10-line direct implementation instead of a multi-component architecture?"
                )
            }
        ),
        "direction_alignment_score": ScoreQuestion(
            instructions=(
                "Rate the alignment of the current work with the true root goal from first principles."
            ),
            criteria=[
                "Off-track or severely biased (requires immediate halt and restructuring)",
                "Partially aligned with minor drift or unverified assumptions (caution warranted)",
                "100% aligned with first principles and zero cognitive bias"
            ]
        )
    }

    raw_eval = evaluate_state(state_payload, questions)
    answers = raw_eval.get("answers", {})

    pattern = answers.get("holistic_bias_pattern", {}).get("choice", "sound_and_aligned")
    confidence = answers.get("holistic_bias_pattern", {}).get("confidence", 0.8)
    is_sound = answers.get("is_direction_fundamentally_sound", {}).get("noul", 1.0) >= 0.5
    unlock_q = answers.get("one_question_that_unlocks_everything", {}).get("choice", "verify_root_deliverable")
    score_val = answers.get("direction_alignment_score", {}).get("score", 2.0)

    requires_halt = (pattern != "sound_and_aligned") and (not is_sound or score_val < 0.9)
    status = "HALT & RESTRUCTURE" if requires_halt else ("CAUTION" if pattern != "sound_and_aligned" else "CLEAR")

    return {
        "stage": 1,
        "checkpoint_band": "40% - 50%",
        "status": status,
        "requires_halt": requires_halt,
        "detected_pattern": pattern,
        "confidence": confidence,
        "is_direction_sound": is_sound,
        "one_question_that_unlocks_everything": unlock_q,
        "alignment_score": score_val,
        "raw_answers": answers
    }


def run_stage2_convergence_audit(
    task_context: str,
    current_work: str,
    verification_evidence: Optional[str] = None,
    workspace: Optional[str] = None
) -> Dict[str, Any]:
    """
    STAGE 2: 60% - 70% DEEP CONVERGENCE & FALSE COMPLETION AUDIT
    Audits for:
    - True 100% Completion vs Superficial 50% Disguised as 100%
    - Agent Hallucination (fabricated methods, nonexistent parameters)
    - Hidden Technical Regressions & Execution Debt
    - Actionable Course Correction Directive
    """
    state_payload = {
        "original_task": task_context,
        "current_implementation_state": current_work,
        "verification_evidence_or_test_results": verification_evidence or "No tests/verification provided",
        "workspace": workspace or "Default"
    }

    questions = {
        "convergence_integrity_pattern": ChoiceQuestion(
            instructions=(
                "From a strict third-person technical auditing perspective at 60-70% completion: "
                "Audit the code and deliverables. Is the work truly converging to 100% completion, "
                "or is there a hidden failure mode?"
            ),
            criteria={
                "false_completion_trap": (
                    "The work appears finished on the surface, but critical edge-cases, error handling, "
                    "or requirements are skipped (superficial completion / AI slop)."
                ),
                "agent_hallucination": (
                    "The agent fabricated nonexistent methods, hallucinated configuration parameters, "
                    "or authored code that looks plausible but is mechanically invalid."
                ),
                "hidden_regressions": (
                    "The changes break existing system rules, degrade performance, or violate core constraints."
                ),
                "overengineered_bloat": (
                    "The code is unnecessarily complicated, fragile, and hard to maintain."
                ),
                "flawless_convergence": (
                    "The implementation is verified, robust, adheres to all constraints, and is truly "
                    "on track for 100% production excellence."
                )
            }
        ),
        "is_truly_100_percent_converged": NoulQuestion(
            instructions=(
                "Will this implementation deliver 100% of the true target without hidden defects or missing pieces? "
                "True = genuine 100% convergence."
            )
        ),
        "course_correction_directive": ChoiceQuestion(
            instructions=(
                "What is the single most critical mechanical action required right now to lock in 100% quality?"
            ),
            criteria={
                "run_end_to_end_verification": (
                    "Execute real commands/unit tests to verify execution without relying on assumptions."
                ),
                "purge_unnecessary_complexity": (
                    "Strip out dead code, unneeded abstractions, and simplify the critical path."
                ),
                "fill_missing_edge_cases": (
                    "Address missing error handlers, boundary conditions, and failure states."
                ),
                "align_with_strict_rules": (
                    "Audit against permanent user rules (zero emojis, drive safety, decision gating) and fix violations."
                )
            }
        ),
        "convergence_score": ScoreQuestion(
            instructions=(
                "Rate the technical convergence depth of the implementation."
            ),
            criteria=[
                "Critical defects or false completion (requires immediate halt and remediation)",
                "Acceptable progress but requires verification and polish before release",
                "100% verified, clean architecture, production ready"
            ]
        )
    }

    raw_eval = evaluate_state(state_payload, questions)
    answers = raw_eval.get("answers", {})

    pattern = answers.get("convergence_integrity_pattern", {}).get("choice", "flawless_convergence")
    confidence = answers.get("convergence_integrity_pattern", {}).get("confidence", 0.8)
    is_converged = answers.get("is_truly_100_percent_converged", {}).get("noul", 1.0) >= 0.5
    directive = answers.get("course_correction_directive", {}).get("choice", "run_end_to_end_verification")
    score_val = answers.get("convergence_score", {}).get("score", 2.0)

    requires_halt = (pattern != "flawless_convergence") and (not is_converged or score_val < 0.9)
    status = "HALT & RESTRUCTURE" if requires_halt else ("CAUTION" if pattern != "flawless_convergence" else "CLEAR")

    return {
        "stage": 2,
        "checkpoint_band": "60% - 70%",
        "status": status,
        "requires_halt": requires_halt,
        "detected_pattern": pattern,
        "confidence": confidence,
        "is_converged": is_converged,
        "course_correction_directive": directive,
        "convergence_score": score_val,
        "raw_answers": answers
    }


# ----------------------------------------------------------------------
# Visual Card Formatter (STRICT ZERO EMOJIS - Complies with Rule 3)
# ----------------------------------------------------------------------

def format_tpa_verdict_card(verdict: Dict[str, Any], task: str, progress_pct: float) -> str:
    stage = verdict.get("stage", 1)
    status = verdict.get("status", "CLEAR")
    band = verdict.get("checkpoint_band", "40% - 50%" if stage == 1 else "60% - 70%")
    pattern = verdict.get("detected_pattern", "sound_and_aligned")
    conf = int(verdict.get("confidence", 0.8) * 100)
    score = verdict.get("alignment_score" if stage == 1 else "convergence_score", 2.0)

    if stage == 1:
        action_title = "The One Unlock Question"
        action_val = verdict.get("one_question_that_unlocks_everything", "verify_root_deliverable")
    else:
        action_title = "Course Correction Directive"
        action_val = verdict.get("course_correction_directive", "run_end_to_end_verification")

    card_lines = [
        "================================================================================",
        f"THIRD-PERSON AUDIT (TPA) - [STAGE {stage}: {band} CHECKPOINT]",
        "================================================================================",
        f"Status:             {status}",
        f"Current Progress:   {progress_pct:.1f}%",
        f"Task Context:       {task[:65]}...",
        f"Detected Pattern:   {pattern}",
        f"System 1 Conf:      {conf}%",
        f"Integrity Score:    {score:.2f} / 2.0",
        "--------------------------------------------------------------------------------",
        f"{action_title}:",
        f"  >> {action_val}",
        "================================================================================"
    ]
    if verdict.get("requires_halt"):
        card_lines.insert(6, "WARNING: CRITICAL DRIFT/BIAS DETECTED. EXECUTION HALTED FOR HUMAN REVIEW.")

    return "\n".join(card_lines)


# ----------------------------------------------------------------------
# Master Public Agent Hook
# ----------------------------------------------------------------------

def tpa_step(
    task: str,
    current_step: int,
    total_steps: int = 10,
    progress_pct: Optional[float] = None,
    step_summary: Optional[str] = None,
    human_directives: Optional[str] = None,
    workspace: Optional[str] = None,
    session_id: Optional[str] = None,
    force_stage: Optional[int] = None
) -> Dict[str, Any]:
    """
    ONE-LINE AGENT INGRESS HOOK:
    Call on each step or milestone. Automatically evaluates if progress has crossed
    the 40% (Stage 1) or 60% (Stage 2) watermark bands, triggering TPA without manual intervention.
    """
    sid = session_id or _get_task_hash(task, workspace)
    session = TPASessionLedger.get_session(sid)

    if progress_pct is not None:
        pct = float(progress_pct)
    elif total_steps > 0:
        pct = min(100.0, max(0.0, (current_step / total_steps) * 100.0))
    else:
        pct = 0.0

    session["progress_pct"] = pct
    session["current_step"] = current_step
    session["total_steps"] = total_steps

    triggered = False
    active_stage = None
    verdict = None

    if force_stage in (1, 2):
        active_stage = force_stage
        triggered = True
    elif pct >= 40.0 and not session.get("stage1_latched", False):
        active_stage = 1
        triggered = True
        session["stage1_latched"] = True
    elif pct >= 60.0 and not session.get("stage2_latched", False):
        active_stage = 2
        triggered = True
        session["stage2_latched"] = True

    if triggered and active_stage == 1:
        verdict = run_stage1_midflight_audit(
            task_context=task,
            current_work=step_summary or f"Step {current_step}/{total_steps} in progress",
            human_directives=human_directives,
            workspace=workspace
        )
        session["stage1_verdict"] = verdict
        session["audit_history"].append({"stage": 1, "timestamp": time.time(), "verdict": verdict})

    elif triggered and active_stage == 2:
        verdict = run_stage2_convergence_audit(
            task_context=task,
            current_work=step_summary or f"Step {current_step}/{total_steps} in progress",
            verification_evidence=step_summary,
            workspace=workspace
        )
        session["stage2_verdict"] = verdict
        session["audit_history"].append({"stage": 2, "timestamp": time.time(), "verdict": verdict})

    TPASessionLedger.save_all({**TPASessionLedger.load_all(), sid: session})

    card = None
    requires_halt = False
    status = "IN_PROGRESS"

    if triggered and verdict:
        card = format_tpa_verdict_card(verdict, task, pct)
        requires_halt = verdict.get("requires_halt", False)
        status = verdict.get("status", "CLEAR")

    return {
        "triggered": triggered,
        "stage": active_stage,
        "progress_pct": pct,
        "requires_halt": requires_halt,
        "status": status,
        "verdict_card": card,
        "verdict": verdict,
        "session_id": sid
    }


def run_tpa_audit(
    task: str,
    stage: int = 1,
    current_work: str = "",
    human_directives: Optional[str] = None,
    workspace: Optional[str] = None
) -> Dict[str, Any]:
    """Direct manual / on-demand audit runner."""
    if stage == 1:
        return run_stage1_midflight_audit(task, current_work, human_directives, workspace)
    elif stage == 2:
        return run_stage2_convergence_audit(task, current_work, current_work, workspace)
    else:
        raise ValueError("Stage must be 1 (40-50% Mid-flight) or 2 (60-70% Convergence).")
