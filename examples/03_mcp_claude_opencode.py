#!/usr/bin/env python3
"""
Example 3: Configuring the System One & TPA MCP Server for IDEs
Shows how to register the MCP server with Claude Code, OpenCode, Antigravity, and Cursor.
"""

import json

def get_claude_code_config():
    """Configuration snippet for claude_desktop_config.json or opencode.jsonc."""
    return {
        "mcpServers": {
            "system1-tpa": {
                "command": "python",
                "args": ["-m", "system1.mcp_server"],
                "env": {
                    "TYPESAFE_API_KEY": "YOUR_TYPESAFE_KEY_HERE",
                    "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_HERE"
                }
            }
        }
    }

if __name__ == "__main__":
    print("Add this JSON block to your MCP client configuration:")
    print(json.dumps(get_claude_code_config(), indent=2))
