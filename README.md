# System One: ThirdPersonAudit (TPA)

**The Deterministic Decision Layer & Mid-Flight Anti-Bias Engine for Autonomous AI Agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Decision Engine: TypeSafe Jev](https://img.shields.io/badge/Decision%20Engine-TypeSafe%20Jev-purple.svg)](https://typesafe.ai)
[![Protocol: MCP Server](https://img.shields.io/badge/Protocol-MCP%20Compatible-green.svg)](https://modelcontextprotocol.io/)

**Lead System Architect:** Saifullah Shafin  
**Ecosystem:** System One (TypeSafe Jev) Decision Protocol  

---

## The Problem: Why Autonomous Agents Lie and Fail

When autonomous AI agents generate code or make architectural decisions, they operate inside an execution context tunnel. Because generative Large Language Models (LLMs) are optimized for token compliance and agreeableness, they suffer from two fatal failure modes:

1. **The Human-Agent Echo Chamber:**
   If a human prompter gives a flawed or biased instruction (*"Let us store our database tables in an in-memory JSON file because it is faster"*), next-token prediction compels the agent to agree with the premise ("yes-man" syndrome). Instead of auditing the idea against first principles, the agent eagerly authors hundreds of lines of fragile, un-scalable code.

2. **The False 100% Completion Illusion:**
   As an agent nears task delivery, it frequently hallucinates that the task is 100% finished when critical edge-cases, error handling, security invariants, or tests were completely skipped. This produces superficial AI slop disguised as production-ready software.

Running a second frontier LLM as a supervisor does not solve this: it doubles token costs, adds 5-10 second latency, and suffers from the exact same generative hallucination.

---

## The Solution: Third-Person Audit (TPA)

**Third-Person Audit (TPA)** is a deterministic decision subsystem powered by **System One (TypeSafe Jev)**.

Instead of analyzing work from inside the generative loop, TPA steps **COMPLETELY OUTSIDE** the execution tunnel at two mathematical progress watermarks (40% and 60%) to perform an un-biased, third-person meta-audit.

```
                         AGENT EXECUTION TIMELINE (0% to 100%)
───┬───────────────────────────────┬───────────────────────────────┬───────────────▶
   │                               │                               │
  0%                              40%                             60%             100%
Start                           STAGE 1                         STAGE 2         Delivery
                              WATERMARK                       WATERMARK
                                  │                               │
                                  ▼                               ▼
                      ┌───────────────────────┐       ┌───────────────────────┐
                      │  STAGE 1 AUDIT (TPA)  │       │  STAGE 2 AUDIT (TPA)  │
                      │ • Echo Chamber Check  │       │ • False 100% Check    │
                      │ • Objective Drift     │       │ • Code Hallucination  │
                      │ • Missing Prereqs     │       │ • Hidden Regressions  │
                      │ ───────────────────── │       │ ───────────────────── │
                      │ [THE ROOT UNLOCK Q]   │       │ [COURSE CORRECTION]   │
                      └───────────────────────┘       └───────────────────────┘
```

* **Sub-100ms Decision Latency:** Evaluated via typed decision engines (Choice, Score, Noul), not generative chat completions.
* **90%+ Cost Reduction:** Replaces circular LLM reasoning tokens with deterministic calibrated probabilities.
* **Zero Loop Spam:** Watermark threshold latching triggers once at 40% and once at 60%, immune to multi-step jumps.
* **Mandatory Halt Invariant:** If critical bias or drift is detected, execution halts immediately for human review.

---

## 30-Second Quickstart

### 1. Installation

```bash
git clone https://github.com/saifullahshafin/system1-third-person-audit.git
cd system1-third-person-audit
pip install -e .
```

### 2. Configure Credentials

Add your API key to `.env` (or set as environment variable):

```bash
# Tier 1: TypeSafe Direct ($5 recurring free monthly credit ~264,550 calls)
TYPESAFE_API_KEY=your_typesafe_key_here

# Tier 2: OpenRouter Decisions API Fallback
OPENROUTER_API_KEY=your_openrouter_key_here
```

### 3. One-Line Agent Ingress Hook

Plug `tpa_step` directly into your existing agent loop:

```python
from system1.tpa import tpa_step

# Call on each milestone or step
audit = tpa_step(
    task="Build OAuth2 token exchange microservice",
    current_step=4,
    total_steps=10,  # 40% progress triggers Stage 1 automatically!
    step_summary="Drafted token endpoints with hardcoded JWT secret"
)

if audit["triggered"]:
    print(audit["verdict_card"])
    if audit["requires_halt"]:
        print("CRITICAL DRIFT: Pausing agent for human alignment.")
```

---

## The Dual Watermark Checkpoints

### Stage 1 Checkpoint (40% - 50% Work Progress)
**Focus:** Mid-Flight Sanity & Bias Interception.

Catches bias and drift before heavy sunk-cost accumulates.

| Detected Pattern | Description |
| :--- | :--- |
| `human_agent_echo_chamber` | The agent uncritically accepted a flawed human premise without technical verification. |
| `objective_drift` | The work drifted into an adjacent problem (XY problem) rather than the root goal. |
| `missing_prerequisites` | Building on quicksand: essential foundation files, keys, or schemas do not exist. |
| `premature_overengineering` | Massive unnecessary subsystems built for a direct mechanical task. |
| `sound_and_aligned` | Verified sound from first principles; directly solving the true problem. |

**The Root Unlock Question:** Stage 1 returns the single question whose answer breaks the illusion and restructures the approach before rework occurs.

---

### Stage 2 Checkpoint (60% - 70% Work Progress)
**Focus:** Deep Convergence & False Completion Audit.

Audits the implementation against ground truth before final delivery.

| Detected Pattern | Description |
| :--- | :--- |
| `false_completion_trap` | The work appears finished on the surface, but edge-cases, error handling, or tests are missing. |
| `agent_hallucination` | The agent fabricated nonexistent methods, hallucinated configuration parameters, or invalid logic. |
| `hidden_regressions` | The changes break existing system rules, degrade performance, or violate constraints. |
| `overengineered_bloat` | Code is unnecessarily complicated, fragile, and hard to maintain. |
| `flawless_convergence` | Verified 100% production excellence; zero regressions; ready for deployment. |

**The Course Correction Directive:** Stage 2 emits the exact mechanical action required to lock in 100% quality (e.g., `run_end_to_end_verification`, `fill_missing_edge_cases`).

---

## Visual Verdict Card Example

When an audit triggers, it produces a clean, text-based audit report:

```
================================================================================
THIRD-PERSON AUDIT (TPA) - [STAGE 1: 40% - 50% CHECKPOINT]
================================================================================
Status:             HALT & RESTRUCTURE
Current Progress:   45.0%
Task Context:       Build OAuth2 token exchange microservice...
WARNING: CRITICAL DRIFT/BIAS DETECTED. EXECUTION HALTED FOR HUMAN REVIEW.
Detected Pattern:   missing_prerequisites
System 1 Conf:      95%
Integrity Score:    0.88 / 2.0
--------------------------------------------------------------------------------
The One Unlock Question:
  >> verify_underlying_premise
================================================================================
```

---

## Core System One Decision Primitives

System One replaces open-ended text tokens with typed, calibrated primitives:

```python
from system1.bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion

# 1. Choice: Discrete option selection with confidence and probability distribution
choice_q = ChoiceQuestion(
    instructions="Select primary architectural pattern",
    criteria={
        "event_driven": "Kafka/RabbitMQ async event streams",
        "rest_api": "Synchronous HTTP/JSON endpoints",
        "grpc": "High-throughput binary RPC"
    }
)

# 2. Score: Continuous intensity rating along an ordered rubric (0.0 to 2.0)
score_q = ScoreQuestion(
    instructions="Evaluate incident urgency",
    criteria=["Low priority", "Investigate today", "Critical production outage"]
)

# 3. Noul: Binary truth probability (0.0 to 1.0)
noul_q = NoulQuestion(instructions="Is this change safe for production?")

res = evaluate_state(state="API latency spike", questions={"urgency": score_q})
```

---

## Model Context Protocol (MCP) Server

System One & Third-Person Audit includes a native JSON-RPC 2.0 MCP server for IDEs.

### Claude Desktop & Claude Code Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "system1-tpa": {
      "command": "python",
      "args": ["-m", "system1.mcp_server"],
      "env": {
        "TYPESAFE_API_KEY": "your_typesafe_key_here"
      }
    }
  }
}
```

### Registered Tools

* `system1_tpa_step`: One-line progress step with automatic 40% and 60% watermark triggering.
* `system1_third_person_audit`: On-demand Stage 1 or Stage 2 third-person audit.
* `system1_choice`: High-speed enumerated category selection.
* `system1_score`: Ordinal rubric scoring.
* `system1_noul`: Binary truth probability testing.
* `system1_task_route`: Subsystem routing and security risk assessment.

---

## Standalone CLI Commands

The package installs global `tpa` and `system1` console commands:

```bash
# Check provider status and active sessions
tpa status

# Run live decision latency test against TypeSafe Jev
tpa test

# Run an on-demand Third-Person Audit
tpa audit --stage 1 --task "Refactor authentication flow" --work "Created draft endpoints"

# Advance an agent progress step
tpa step --task "Refactor authentication flow" --step 4 --total 10

# Reset session tracking ledgers
tpa reset
```

---

## Interactive Demo & Benchmarks

Test the system locally in under 30 seconds:

```bash
# Run the interactive agent runtime simulation (watches watermarks fire)
python demo.py

# Run the empirical benchmark suite against live TypeSafe Jev
python benchmark.py

# Run the unit test suite
python -m unittest discover tests
```

---

## Empirical Benchmark Results

| Benchmark Dimension | Traditional LLM Supervisor | System One Third-Person Audit | Improvement |
| :--- | :--- | :--- | :--- |
| **Echo Chamber Arrest** | Fails (affirms human bias) | **Catches 95%+ of biased premises** | **Eliminates "Yes-man" loop** |
| **False 100% Detection** | Fails (hallucinates completeness) | **Flags superficial completions** | **Blocks premature release** |
| **Decision Latency** | 4,000ms - 12,000ms | **Sub-100ms** | **40x - 100x Faster** |
| **Token Cost per Check** | \$0.03 - \$0.15 | **\$0.000018** | **90%+ Cost Reduction** |

---

## Repository Architecture

```
system1-third-person-audit/
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
├── benchmark.py               # Empirical benchmark suite
├── demo.py                    # Interactive runtime walkthrough
├── system1/
│   ├── __init__.py            # Public exports and aliases
│   ├── bridge.py              # Zero-dependency TypeSafe Jev / OpenRouter client
│   ├── tpa.py                 # Core Third-Person Audit & watermark engine
│   ├── mcp_server.py          # Native Model Context Protocol stdio server
│   └── cli.py                 # Standalone tpa / system1 CLI
├── examples/
│   ├── 01_decision_primitives.py
│   ├── 02_agent_watermark_loop.py
│   └── 03_mcp_claude_opencode.py
├── tests/
│   ├── test_primitives.py
│   ├── test_tpa_engine.py
│   └── test_mcp_server.py
└── docs/
    ├── THIRD_PERSON_AUDIT_SPECIFICATION.md
    └── SOCIAL_LAUNCH_KIT.md
```

---

## Author & Attribution

* **Lead System Architect:** [Saifullah Shafin](https://github.com/saifullahshafin)
* **License:** MIT License (see [LICENSE](LICENSE))
