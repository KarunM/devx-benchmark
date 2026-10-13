#!/usr/bin/env python3
"""Dummy stdio MCP server: one tool `ping`, empty schema. Used for fixed-cost isolation."""
import sys, json

TOOL = {"name": "ping", "description": "Returns pong.",
        "inputSchema": {"type": "object", "properties": {}}}

def send(obj):
    sys.stdout.write(json.dumps(obj) + "\n"); sys.stdout.flush()

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    m = json.loads(line); mid = m.get("id"); meth = m.get("method")
    if mid is None: continue
    if meth == "initialize":
        send({"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": m["params"].get("protocolVersion", "2024-11-05"),
              "capabilities": {"tools": {}}, "serverInfo": {"name": "dummy", "version": "1"}}})
    elif meth == "tools/list":
        send({"jsonrpc": "2.0", "id": mid, "result": {"tools": [TOOL]}})
    elif meth == "tools/call":
        send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": "pong"}]}})
    else:
        send({"jsonrpc": "2.0", "id": mid, "result": {}})
