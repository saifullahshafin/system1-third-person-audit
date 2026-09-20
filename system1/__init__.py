"""
System One: Master Deterministic Decision Architecture & Third-Person Audit (TPA)
Author: Saifullah Shafin (Lead System Architect)
"""

from .bridge import (
    evaluate_state,
    ChoiceQuestion,
    ScoreQuestion,
    NoulQuestion,
    get_client_config,
    load_env_credentials
)
from .tpa import (
    tpa_step,
    run_tpa_audit,
    format_tpa_verdict_card,
    TPASessionLedger
)
from .security import (
    audit_code,
    audit_command
)
from .router import (
    route_task
)
from .evaluator import (
    evaluate_video_transcript
)

# Backward-compatible aliases
hmo_step = tpa_step
run_holistic_audit = run_tpa_audit
HMOSessionLedger = TPASessionLedger
format_hmo_verdict_card = format_tpa_verdict_card

__all__ = [
    # Core System One Bridge
    "evaluate_state",
    "ChoiceQuestion",
    "ScoreQuestion",
    "NoulQuestion",
    "get_client_config",
    "load_env_credentials",

    # Third-Person Audit (TPA) Engine
    "tpa_step",
    "run_tpa_audit",
    "format_tpa_verdict_card",
    "TPASessionLedger",
    "hmo_step",
    "run_holistic_audit",
    "HMOSessionLedger",
    "format_hmo_verdict_card",

    # Security & Code Diff Auditor
    "audit_code",
    "audit_command",

    # Autonomous Task Router
    "route_task",

    # Content & Video Signal Evaluator
    "evaluate_video_transcript",
]

__version__ = "1.0.0"
__author__ = "Saifullah Shafin"
