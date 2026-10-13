# TRIAL-C: arm C (devx CLI via shell), attempt 2

**Attempt 1 (blocked):** 3 paid runs (series trial-c) all incorrect; every `devx` call exited 134 with `SQLite Error 8: 'attempt to write a readonly database'` (SqliteSessionStore.SaveAsync / SaveSearchAsync). Cause: Codex `-s read-only` forbids DevX writing search/read history to `F2/.devx/devx.db`. No data used.

**Attempt 2** (series trial-c2): `run_bench.py --sandbox workspace-write` (default stays `read-only`; D and N unchanged). **Arm C ran with the write-permitting sandbox; D and N ran read-only.** Pre-run proof: `devx search symbol "factorint" ...` from the F2 root with the clibin PATH, exit 0.

| task | arm | correct | calls devx/shell/mcp | input tok | output tok | result bytes | wall s |
|---|---|---|---|---|---|---|---|
| L1 | C | 1 | 1/0/0 | 28066 | 151 | 383 | 5.5 |
| R1 | C | 1 | 1/0/0 | 27120 | 179 | 628 | 6.4 |
| M1 | C | 1 | 3/0/0 | 59447 | 427 | 9596 | 10.9 |
| L1 | D | 1 | 0/0/1 | 58142 | 159 | 382 | 9.7 |
| R1 | D | 1 | 0/0/1 | 58707 | 186 | 627 | 9.6 |
| M1 | D | 1 | 0/0/5 | 105795 | 517 | 13298 | 23.8 |
| L1 | N | 1 | 0/1/0 | 26166 | 114 | 105 | 8.4 |
| R1 | N | 1 | 0/1/0 | 26998 | 118 | 2674 | 5.0 |
| M1 | N | 1 | 0/2/0 | 41134 | 311 | 3923 | 8.4 |

Means: C calls 1.67, input 38211, output 252, bytes 3536, wall 7.6 s. D calls 2.33, input 74215, bytes 4769. N calls 1.33, input 31433, bytes 2234.
Savings line: C as % of N: calls 125%, input tokens 122%, result bytes 158%. (C as % of D: calls 71%, input 51%, bytes 74%.)

## devx commands (in order; all exit 0)
- L1: `search symbol "factorint"` 383 B, needed.
- R1: `read method "sympy.core.symbol.Dummy.__new__"` 628 B, needed.
- M1: `search symbol "Symbol"` 1161 B (arguably not needed); `read type "sympy.core.symbol.Symbol"` 7404 B, needed; `search text "def to_nnf"` 1031 B, needed.
No grep/sed fallback, no devx error. stderr only "Reading additional input from stdin...".

## Writes
F2 is not a git repo; file listing (path, mtime, size) before/after: only `./.devx/devx.db` changed (mtime; size equal). Nothing outside `.devx` was written (results/f2-before.txt, f2-after.txt).

## Verdict
No (mixed at best): all 3 correct, but arm C used more calls (1.67 vs 1.33), input tokens (+22%) and result bytes (+58%) than the shell-only arm N on these three tasks; the tasks are single-grep-solvable, and `read type Symbol` returned 7404 B for M1. Against MCP arm D, C is clearly cheaper (about half the input tokens), confirming the MCP penalty is Codex's. n=1 per cell and C had a different sandbox, so this is a trial, not evidence either way for larger tasks.
