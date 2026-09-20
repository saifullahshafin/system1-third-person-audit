# System One & Third-Person Audit: Golden Path Guide

**Lead System Architect:** Saifullah Shafin  
**Ecosystem:** System One (TypeSafe Jev) Decision Protocol  

---

## 1. Golden Path Setup & Verification

### Step 1: Environment Variables
Store credentials safely in `.env` (never commit `.env` to version control):

```bash
# Primary Provider: TypeSafe Direct ($5 recurring monthly credit)
TYPESAFE_API_KEY=your_typesafe_key_here

# Automated Fallback Provider: OpenRouter Decisions API
OPENROUTER_API_KEY=your_openrouter_key_here
```

### Step 2: Verification Check
Run the status and live decision test:

```bash
system1 status
system1 test
```

Expected output:
```
System One Client Configuration:
  Active Provider:    typesafe
  Endpoint:           https://api.typesafe.ai/v1/systemone
  Key Detected:       Yes
  Default Model:      jev-latest
```

---

## 2. Hard-Won Failure Patterns & Operational Resolutions

### Failure Pattern 1: HTTP 400 Bad Request on OpenRouter Decisions REST API
* **Symptom:** `urllib.error.HTTPError: HTTP Error 400: Bad Request` when posting to `https://openrouter.ai/api/alpha/decisions`.
* **Root Cause:** The TypeScript SDK wraps payloads in `{ "decisionsRequest": { "model": "...", "state": "...", ... } }`. The raw HTTP REST endpoint on OpenRouter requires flat root-level keys `{ "model": "...", "state": "...", "questions": { ... } }`.
* **Golden Path Resolution:** `system1/bridge.py` automatically flattens root keys before dispatch:
  ```json
  {
    "model": "typesafe/jev-1.13",
    "state": "...",
    "questions": { ... }
  }
  ```

### Failure Pattern 2: Score Equality Check Fails on Decimal Outputs
* **Symptom:** Code checking `if verdict["risk_tier"] == 2` fails to trigger even when risks are critical.
* **Root Cause:** TypeSafe Jev returns probability-weighted continuous decimals (e.g. `1.85`, `1.94`) rather than exact integers.
* **Golden Path Resolution:** Never use exact integer equality for Score answers. Always use threshold comparisons:
  ```python
  is_high_risk = risk_tier >= 1.5
  is_moderate_risk = 0.8 <= risk_tier < 1.5
  ```

### Failure Pattern 3: Circular LLM Supervisor Loops & Token Burn
* **Symptom:** Running an LLM (e.g. Claude / GPT-4) to supervise another LLM costs \$0.10+ per step, adds 10s latency, and affirms the same hallucinations.
* **Golden Path Resolution:** Decouple supervision completely. Run `tpa_step()` at 40% and 60% progress watermarks. TPA runs in 80ms for \$0.000018 per audit with zero text hallucination.

---

## 3. Model Context Protocol (MCP) Integration Recipes

### Claude Code & Claude Desktop Setup
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "system1": {
      "command": "python",
      "args": ["-m", "system1.mcp_server"],
      "env": {
        "TYPESAFE_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

### OpenCode Setup
Add to `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "mcp": {
    "system1": {
      "command": "python",
      "args": ["-m", "system1.mcp_server"],
      "env": {
        "TYPESAFE_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

---

## 4. Systems Axioms

1. **The Separation of Powers:**  
   Separate the calibrated Decision Layer (System One + TPA) from the Generative Execution Layer. Never use expensive frontier LLMs for intermediate agent routing.
2. **The Mathematical Law of System One:**  
   Quality of Decision <= Quality of Question Frame. Decision systems fail not from lack of model intelligence, but from lack of question precision.
3. **The Zero-Gut Invariant:**  
   Reject subjective generative assumptions. Every critical routing, architectural, and security gate must be evaluated deterministically through typed rubrics.
