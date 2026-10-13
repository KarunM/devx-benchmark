# Trial (gpt-6-luna via Codex, F2 sympy copy, 1 rep, ripgrep engine, CS21 d9340e9)

| task | arm | correct | calls (shell/mcp) | input_tokens | output_tokens | result_bytes | wall_s |
|---|---|---|---|---|---|---|---|
| L1 locate | D | 1 | 1 (0/1) | 58142 | 159 | 382 | 9.7 |
| L1 locate | N | 1 | 1 (1/0) | 26166 | 114 | 105 | 8.4 |
| R1 read | N | 1 | 1 (1/0) | 26998 | 118 | 2674 | 5.0 |
| R1 read | D | 1 | 1 (0/1) | 58707 | 186 | 627 | 9.6 |
| M1 multihop | D | 1 | 5 (0/5) | 105795 | 517 | 13298 | 23.8 |
| M1 multihop | N | 1 | 2 (2/0) | 41134 | 311 | 3923 | 8.4 |

Per arm (mean of 3): D correct 1.00, calls 2.3 (0.0/2.3), input 74215, output 287, wall 14.4 s. N correct 1.00, calls 1.3 (1.3/0.0), input 31433, output 181, wall 7.3 s.
Savings: arm D calls = 175% of arm N; arm D input tokens = 236% of arm N (D is worse on both in the trial).

Arm D tool usage (JSONL mcp_tool_call items): L1 search x1; R1 read x1; M1 read x3 + search x2. No shell fallback, no tool errors, no protocol errors. Arm N: shell only (command_execution), no DevX available (scratch CODEX_HOME without the global AGENTS.md, PATH without ~/.dotnet/tools).

Findings
- Fixed cost: arm D input is ~+32k tokens on every run (L1: 58142 vs 26166 for one call each). Attributed to the MCP tool list (16 tools with schemas, incl. edit/patch/build/test) in the prompt; not isolated by an extra run. This outweighs any per-call saving on easy tasks.
- M1 cost D 5 calls vs N 2: the agent used `kind:"text"` searches and type reads (13298 result bytes) where one grep found the answer.
- Both arms 3/3 correct; trial tasks are easy single-hop for grep on 1.6k files.

Setup issues found (both fixed in run_bench.py)
- MCP calls failed with "requires approval, but approval policy is never" (smoke 1, paid); fix: `-c mcp_servers.devx.default_tools_approval_mode="approve"`.
- ~/.codex/AGENTS.md tells Codex to use the devx CLI; would contaminate arm N. Fixed with CODEX_HOME=<BENCH>/codex_home (symlinked auth, minimal config) and sanitized PATH; ~/.codex untouched.

Recommendations before the full series
1. Test restricting the MCP surface (config `enabled_tools` = search, read, snapshot, callers, references) to cut the fixed ~32k; one more trial pair would confirm. Without this D loses on tokens by construction.
2. Prefer harder tasks (cross-ref, structure) where grep needs many calls; keep the 5-line limit.
3. Prompt D to use `kind:"symbol"` and `callers`/`references` tools; timeout 300 s is ample (max 24 s).
4. Cached tokens are reported (cached_tokens column); consider also reporting uncached input = input - cached.
