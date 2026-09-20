"""
System One: Third-Person Audit (TPA) Engine
Deterministic Decision Layer & Anti-Bias Audit for Autonomous AI Agents.
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

# Backward-compatible aliases
hmo_step = tpa_step
run_holistic_audit = run_tpa_audit
HMOSessionLedger = TPASessionLedger
format_hmo_verdict_card = format_tpa_verdict_card

__all__ = [
    "evaluate_state",
    "ChoiceQuestion",
    "ScoreQuestion",
    "NoulQuestion",
    "get_client_config",
    "load_env_credentials",
    "tpa_step",
    "run_tpa_audit",
    "format_tpa_verdict_card",
    "TPASessionLedger",
    "hmo_step",
    "run_holistic_audit",
    "HMOSessionLedger",
    "format_hmo_verdict_card"
]

__version__ = "1.0.0"
__author__ = "Saifullah Shafin"
