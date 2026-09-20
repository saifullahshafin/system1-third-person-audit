#!/usr/bin/env python3
"""
System One Decision Bridge: TypeSafe Jev Universal Decision Client
Supports:
1. Direct TypeSafe System One API (Model: jev-latest) - Primary
2. OpenRouter Decisions API (Model: typesafe/jev-1.13) - Automated Fallback
3. Human Escalation (Saifullah Shafin / Supervisor) - Ultimate Failsafe

Sub-100ms latency, zero text hallucinations, typed primitives (Choice, Score, Noul).
Zero external runtime dependencies.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional, Union

TYPESAFE_DIRECT_URL = "https://api.typesafe.ai/v1/systemone"
OPENROUTER_DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"


def load_env_credentials() -> Dict[str, str]:
    """Retrieve API keys from environment or local .env files safely."""
    typesafe_key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "").strip()

    candidate_files = [
        ".env",
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.expanduser("~/.env"),
        os.path.expanduser("~/.config/system1/.env")
    ]
    for env_path in candidate_files:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("TYPESAFE_API_KEY="):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val and not typesafe_key:
                                typesafe_key = val
                        elif line.startswith("OPENROUTER_API_KEY="):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val and not openrouter_key:
                                openrouter_key = val
            except Exception:
                pass
        if typesafe_key and openrouter_key:
            break

    return {
        "typesafe_key": typesafe_key,
        "openrouter_key": openrouter_key
    }


def get_client_config() -> Dict[str, str]:
    """Determine the active primary provider and model."""
    creds = load_env_credentials()
    if creds["typesafe_key"]:
        return {
            "provider": "typesafe",
            "url": TYPESAFE_DIRECT_URL,
            "key": creds["typesafe_key"],
            "model": "jev-latest"
        }
    elif creds["openrouter_key"]:
        return {
            "provider": "openrouter",
            "url": OPENROUTER_DECISIONS_URL,
            "key": creds["openrouter_key"],
            "model": "typesafe/jev-1.13"
        }
    else:
        return {
            "provider": "unconfigured",
            "url": TYPESAFE_DIRECT_URL,
            "key": "",
            "model": "jev-latest"
        }


def evaluate_state(
    state: Union[str, Dict[str, Any], list],
    questions: Dict[str, Any],
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a structured System One decision call against Jev.
    Implements multi-tier fallback: TypeSafe Direct -> OpenRouter -> Human Escalation.
    """
    creds = load_env_credentials()
    ts_key = creds["typesafe_key"]
    or_key = creds["openrouter_key"]

    if not ts_key and not or_key:
        raise ValueError(
            "System One Error: Neither TYPESAFE_API_KEY nor OPENROUTER_API_KEY is configured.\n"
            "Decisions must be made deterministically via System One or escalated to human."
        )

    # Tier 1: TypeSafe Direct (Primary)
    if ts_key:
        target_model = model or "jev-latest"
        payload = {"state": state, "model": target_model, "questions": questions}
        body_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {ts_key}",
            "Content-Type": "application/json",
            "User-Agent": "SystemOne-TPA/1.0"
        }
        req = urllib.request.Request(TYPESAFE_DIRECT_URL, data=body_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except Exception as e:
            sys.stderr.write(f"[SystemOne Warning] TypeSafe Direct failed ({e}). Attempting OpenRouter fallback...\n")

    # Tier 2: OpenRouter Decisions Fallback
    if or_key:
        target_model = "typesafe/jev-1.13"
        payload = {"state": state, "model": target_model, "questions": questions}
        body_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {or_key}",
            "Content-Type": "application/json",
            "User-Agent": "SystemOne-TPA/1.0"
        }
        req = urllib.request.Request(OPENROUTER_DECISIONS_URL, data=body_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except Exception as e:
            sys.stderr.write(f"[SystemOne Warning] OpenRouter fallback failed ({e}).\n")

    # Tier 3: Human Escalation Failsafe
    raise RuntimeError(
        "CRITICAL: System One is not responding (both TypeSafe Direct and OpenRouter fallback failed). "
        "Per deterministic protocol, decisions must NOT be made via LLM generative guessing. "
        "The decision must be escalated to the human supervisor."
    )


# Typed Primitive Constructors
def ChoiceQuestion(instructions: str, criteria: Dict[str, str]) -> Dict[str, Any]:
    """Discrete categorical decision from an enumerated taxonomy."""
    return {
        "type": "choice",
        "instructions": instructions,
        "criteria": criteria
    }


def ScoreQuestion(instructions: str, criteria: List[str]) -> Dict[str, Any]:
    """Continuous intensity evaluation along an ordered ordinal rubric."""
    return {
        "type": "score",
        "instructions": instructions,
        "criteria": criteria
    }


def NoulQuestion(instructions: str) -> Dict[str, Any]:
    """Binary truth probability evaluation (0.0 to 1.0)."""
    return {
        "type": "noul",
        "instructions": instructions
    }
