# Isolation (4 paid Codex runs, prompt "Reply with the single word OK...", one request each)

| run | input_tokens | cached_input_tokens | delta vs A0 (input) |
|---|---|---|---|
| A0 no MCP | 13,474 | 1,792 | 0 |
| A1 DevX MCP (15 tools) | 12,971 | 12,032 | -503 |
| A2 dummy MCP (1 tool) | 12,971 | 1,792 | -503 |
| A3 DevX, enabled_tools=["search","read"] (key exists in codex binary) | 12,971 | 0 | -503 |

Verdict: (iii) something else. Neither (i) nor (ii): attaching any MCP server, 1 tool or 15, costs 0 extra input tokens (12,971 each, 503 FEWER than A0). Tool definitions are therefore not in the request at all (Codex defers MCP tools). Cached counts vary run to run (cache state), not with config. Injected content: nothing measurable; the whole MCP-attached delta is -503 tokens. Codex logs (codex_home/logs_2.sqlite) are empty under --ephemeral and --json gives only summed usage, so per-request content cannot be inspected.

Where the 16k comes from (inference, not proven): base is ~13k tokens per model request. Arm N L1 = 26,166 = 1.94 x A0 (2 requests). Arm D L1 = 58,142 = 4.48 x A1 (about 4-5 requests for one tool call), so D makes extra model requests per MCP call (probably deferred-tool discovery plus the call), each resending ~13k. Not tool-list size. Next step (not done, no paid runs left): count requests per tool call with a logging proxy.

## Part B: M1 calls (all MCP, sessionId af688c1a..., format agent)
| # | tool | args | result bytes | needed |
|---|---|---|---|---|
| 1 | read | kind=type, target=sympy/core/symbol.py | 290 | no (file path given as type name: error) |
| 2 | search | kind=text, query "class Symbol" | 639 | yes (shows bases AtomicExpr, Boolean) |
| 3 | read | kind=type, target sympy.core.symbol.Symbol | 7,403 | no (bases already in #2) |
| 4 | search | kind=text, query "def to_nnf" | 694 | yes (lists boolalg.py) |
| 5 | read | kind=type, sympy.logic.boolalg.Boolean | 4,272 | partly (gives :65 and :131) |

Arm N: (1) grep class Symbol / logic imports / def methods | head, 1,767 B, needed; (2) grep class Boolean + two sed ranges, 2,156 B, needed. Total 3,923 B vs D 13,298 B.

Why D needed 5: (d) call 1 was wrong (path passed as a type name, error) and retried, then (b) it read the whole Symbol class (7.4 kB) when the search line already answered the base question; 4 searched first (c) was fine. Task needed only about 3 calls.

CS23 candidate (tool-description wording): in `read` description state that `target` for kind=type must be a qualified name (never a file path) and that a `search` hit line already shows class bases, so a read is only needed for bodies. Would remove calls 1 and 3 (~7.7 kB, 2 requests).
