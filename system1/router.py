#!/usr/bin/env python3
"""
System One Autonomous Task Router & Dispatcher
Sub-100ms classification of agent directives into subsystems and risk tiers.
"""

from typing import Any, Dict, Optional
from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion


def route_task(task_description: str, caller: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluates an autonomous task for subsystem intent, security risk tier,
    and human approval necessity in sub-100ms.
    """
    state = {
        "task_description": task_description,
        "caller": caller or "agent"
    }

    questions = {
        "subsystem_intent": ChoiceQuestion(
            instructions="Which operational subsystem is required to execute `task_description`?",
            criteria={
                "code_engineering": "Code editing, bug fixing, test running, refactoring, or building packages",
                "phantom_research": "Web search, competitor intelligence, documentation scraping, or model comparison",
                "system_ops": "Server configuration, daemon management, environment variables, or database migrations",
                "content_production": "Writing copy, marketing briefs, social media threads, or video scripts",
                "direct_answer": "Factual query answerable with existing context without external tools"
            }
        ),
        "security_risk_tier": ScoreQuestion(
            instructions="What is the operational risk level of executing this task?",
            criteria=[
                "Read-only safe operation",
                "Non-destructive state change or local file modification",
                "Destructive command (file deletion, spending money, public posting, or process killing)"
            ]
        ),
        "requires_human_approval": NoulQuestion(
            instructions="Should this task halt and request explicit human confirmation before proceeding?"
        )
    }

    raw_res = evaluate_state(state, questions)
    answers = raw_res.get("answers", {})

    intent = answers.get("subsystem_intent", {}).get("choice", "code_engineering")
    confidence = answers.get("subsystem_intent", {}).get("confidence", 0.8)
    risk_tier = answers.get("security_risk_tier", {}).get("score", 0.0)
    requires_approval = answers.get("requires_human_approval", {}).get("noul", 0.0) >= 0.5

    return {
        "intent": intent,
        "confidence": confidence,
        "risk_tier": risk_tier,
        "requires_human_approval": requires_approval,
        "raw_answers": answers
    }
