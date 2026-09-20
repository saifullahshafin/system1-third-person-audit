#!/usr/bin/env python3
"""
System One Video & Content Signal Evaluator
Sub-100ms transcript evaluation for signal-to-noise ratio, content pillars,
and monetization opportunities.
"""

from typing import Any, Dict, Optional
from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion


def evaluate_video_transcript(transcript: str, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluates video transcripts or long-form copy in 80ms using TypeSafe Jev.
    """
    state = {
        "title": title or "Untitled Content",
        "transcript_sample": transcript[:12000]
    }

    questions = {
        "signal_to_noise": ScoreQuestion(
            instructions="Evaluate the signal-to-noise ratio and depth of actionable value in `transcript_sample`.",
            criteria=[
                "Low signal, generic filler, clickbait, or repeated beginner advice",
                "Moderate signal, interesting insights but lacks concrete execution steps",
                "High signal, highly actionable tactical blueprint, rare case study, or proprietary framework"
            ]
        ),
        "content_pillar": ChoiceQuestion(
            instructions="What is the primary operational category of this content?",
            criteria={
                "ai_architecture": "AI models, agent frameworks, LLM infrastructure, autonomous systems",
                "client_acquisition": "High-ticket sales, lead generation, outreach pipelines, closing clients",
                "video_and_viral_marketing": "Motion graphics, hooks, video formats, short-form algorithms",
                "digital_business_model": "SaaS, micro-SaaS, agency structures, revenue blueprints",
                "general_mindset": "Philosophy, productivity, habits, or non-technical discussion"
            }
        ),
        "has_monetizable_opportunity": NoulQuestion(
            instructions="Does this content present an explicit side hustle, tool stack, or market gap that can be turned into a revenue-generating service?"
        )
    }

    raw_res = evaluate_state(state, questions)
    answers = raw_res.get("answers", {})

    signal_score = answers.get("signal_to_noise", {}).get("score", 1.0)
    pillar = answers.get("content_pillar", {}).get("choice", "ai_architecture")
    is_monetizable = answers.get("has_monetizable_opportunity", {}).get("noul", 0.0) >= 0.5

    return {
        "signal_score": signal_score,
        "is_high_signal": signal_score >= 1.5,
        "content_pillar": pillar,
        "is_monetizable": is_monetizable,
        "raw_answers": answers
    }
