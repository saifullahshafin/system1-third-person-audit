#!/usr/bin/env python3
"""
System One & Third-Person Audit (TPA) Master MCP Server
Standard JSON-RPC 2.0 Model Context Protocol stdio server.
Compatible with: Claude Code, OpenCode, Antigravity, Cursor, and Windsurf.
"""

import sys
import json
import os

from .bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion
from .tpa import tpa_step, run_tpa_audit, format_tpa_verdict_card
from .security import audit_code, audit_command
from .router import route_task
from .evaluator import evaluate_video_transcript


def create_tools_manifest():
    return [
        {
            "name": "system1_choice",
            "description": "System One high-speed judgment to select exactly one option from an enumerated criteria set. Returns chosen label, confidence score, and probability distribution.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "state": { "type": "string", "description": "Contextual text or data to evaluate." },
                    "instructions": { "type": "string", "description": "The question to answer about the state." },
                    "criteria": { "type": "object", "description": "Dictionary of option keys to definitions." }
                },
                "required": ["state", "instructions", "criteria"]
            }
        },
        {
            "name": "system1_score",
            "description": "System One evaluation along an ordered ordinal rubric. Returns score (0.0 - 2.0) and confidence.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "state": { "type": "string", "description": "Context to evaluate." },
                    "instructions": { "type": "string", "description": "The scoring question." },
                    "criteria": { "type": "array", "items": { "type": "string" }, "description": "Ordered level descriptions." }
                },
                "required": ["state", "instructions", "criteria"]
            }
        },
        {
            "name": "system1_noul",
            "description": "System One binary probability evaluation. Returns probability (0.0 to 1.0) and boolean.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "state": { "type": "string", "description": "Context to evaluate." },
                    "instructions": { "type": "string", "description": "Proposition to test for truth." }
                },
                "required": ["state", "instructions"]
            }
        },
        {
            "name": "system1_tpa_step",
            "description": "One-line step progress checkpoint. Automatically triggers Third-Person Audit (TPA) at 40-50% (Stage 1) and 60-70% (Stage 2) watermarks to arrest agent-human bias, echo chambers, and false completion.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": { "type": "string", "description": "Original task description." },
                    "current_step": { "type": "integer", "description": "Current step number." },
                    "total_steps": { "type": "integer", "description": "Total estimated steps (default 10)." },
                    "progress_pct": { "type": "number", "description": "Explicit progress percentage 0.0 to 100.0." },
                    "step_summary": { "type": "string", "description": "Summary of current work done so far." },
                    "human_directives": { "type": "string", "description": "Any human assumptions or directives passed to the agent." }
                },
                "required": ["task", "current_step"]
            }
        },
        {
            "name": "system1_third_person_audit",
            "description": "On-demand third-person audit. Steps completely outside the execution loop to detect shared cognitive bias, XY problems, or false 100% completion.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": { "type": "string", "description": "Original task description." },
                    "stage": { "type": "integer", "description": "Audit stage: 1 (40-50% Mid-flight bias) or 2 (60-70% Convergence)." },
                    "current_work": { "type": "string", "description": "Current implementation state or verification results." },
                    "human_directives": { "type": "string", "description": "Optional human inputs/assumptions." }
                },
                "required": ["task", "stage"]
            }
        },
        {
            "name": "system1_audit_code",
            "description": "Pre-commit git diff and code safety auditor. Detects hardcoded secrets, breaking API changes, unhandled exceptions, and architectural drift.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "diff": { "type": "string", "description": "Git diff or code snippet to audit." },
                    "context": { "type": "string", "description": "Optional architectural context." }
                },
                "required": ["diff"]
            }
        },
        {
            "name": "system1_task_route",
            "description": "Autonomous task router. Evaluates task directives for subsystem intent, security risk tier, and human approval necessity in sub-100ms.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task_description": { "type": "string", "description": "Description of the task to be executed." }
                },
                "required": ["task_description"]
            }
        },
        {
            "name": "system1_video_eval",
            "description": "Evaluates video transcripts or copy for signal-to-noise ratio, monetization opportunities, and content pillars in 80ms.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "transcript": { "type": "string", "description": "Transcript text to evaluate." },
                    "title": { "type": "string", "description": "Optional video or article title." }
                },
                "required": ["transcript"]
            }
        }
    ]


def handle_tool_call(tool_name, arguments):
    if tool_name == "system1_choice":
        state = arguments.get("state", "")
        instructions = arguments.get("instructions", "")
        criteria = arguments.get("criteria", {})
        questions = { "decision": ChoiceQuestion(instructions, criteria) }
        res = evaluate_state(state, questions)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    elif tool_name == "system1_score":
        state = arguments.get("state", "")
        instructions = arguments.get("instructions", "")
        criteria = arguments.get("criteria", [])
        questions = { "decision": ScoreQuestion(instructions, criteria) }
        res = evaluate_state(state, questions)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    elif tool_name == "system1_noul":
        state = arguments.get("state", "")
        instructions = arguments.get("instructions", "")
        questions = { "decision": NoulQuestion(instructions) }
        res = evaluate_state(state, questions)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    elif tool_name == "system1_tpa_step":
        task = arguments.get("task", "")
        current_step = arguments.get("current_step", 1)
        total_steps = arguments.get("total_steps", 10)
        progress_pct = arguments.get("progress_pct")
        step_summary = arguments.get("step_summary", "")
        human_directives = arguments.get("human_directives", "")

        step_res = tpa_step(
            task=task,
            current_step=current_step,
            total_steps=total_steps,
            progress_pct=progress_pct,
            step_summary=step_summary,
            human_directives=human_directives
        )
        return { "content": [{ "type": "text", "text": json.dumps(step_res, indent=2) }] }

    elif tool_name == "system1_third_person_audit":
        task = arguments.get("task", "")
        stage = arguments.get("stage", 1)
        current_work = arguments.get("current_work", "")
        human_directives = arguments.get("human_directives", "")

        audit_res = run_tpa_audit(
            task=task,
            stage=stage,
            current_work=current_work,
            human_directives=human_directives
        )
        card = format_tpa_verdict_card(audit_res, task, 45.0 if stage == 1 else 65.0)
        output_payload = {
            "verdict": audit_res,
            "verdict_card": card
        }
        return { "content": [{ "type": "text", "text": json.dumps(output_payload, indent=2) }] }

    elif tool_name == "system1_audit_code":
        diff = arguments.get("diff", "")
        context = arguments.get("context", "")
        res = audit_code(diff, context)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    elif tool_name == "system1_task_route":
        task = arguments.get("task_description", "")
        res = route_task(task)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    elif tool_name == "system1_video_eval":
        transcript = arguments.get("transcript", "")
        title = arguments.get("title", "")
        res = evaluate_video_transcript(transcript, title)
        return { "content": [{ "type": "text", "text": json.dumps(res, indent=2) }] }

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


def run_stdio_server():
    """Main JSON-RPC 2.0 stdio server loop for MCP."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "system1-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                continue

            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": create_tools_manifest()
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                args = params.get("arguments", {})
                try:
                    call_result = handle_tool_call(tool_name, args)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": call_result
                    }
                except Exception as e:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {
                            "code": -32000,
                            "message": str(e)
                        }
                    }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Server error: {e}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
