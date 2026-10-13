# Series 2: 12 tasks x arms C and N, 1 rep, gpt-6-luna, CS24 build 1.6.14+df25de6, arm C guided only by DevX's shipped AGENTS.md block

Setup: `devx version` = 1.6.14+df25de63e25da35db52a97b43eb3912083c9bb1b (seen before runs); index Current, 1605 files, no reindex; `read type sympy.core.symbol.Symbol` = 1216 bytes. Shipped block (`devx init --agents codex`) = 2933 bytes, contains "callers" and "Bare or"; the single edit (the `SESSION_ID=$(devx session create ...)` line replaced by `SESSION_ID=af688c1a-...`) gives 2893 bytes in codex_home_c/AGENTS.md. Arm C: reduced preamble, workspace-write; arm N: unchanged, read-only, codex_home without AGENTS.md. Exactly 24 paid runs, no reruns, all rc=0, no timeouts. F2 before/after listing (excluding .devx): no differences.

## Tables
| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |
|--|--|--|--|--|--|--|--|--|
| L1 | locate | C | 1 | 1 (1/0) | 28279 | 130 | 383 | 8.3 |
| L1 | locate | N | 1 | 1 (0/1) | 27164 | 111 | 105 | 8.5 |
| L2 | locate | C | 1 | 1 (1/0) | 28232 | 129 | 287 | 4.7 |
| L2 | locate | N | 1 | 1 (0/1) | 28436 | 133 | 4617 | 5.8 |
| L3 | locate | C | 1 | 1 (1/0) | 28421 | 128 | 1023 | 5.4 |
| L3 | locate | N | 1 | 1 (0/1) | 26106 | 84 | 53 | 5.2 |
| M1 | multihop | C | 1 | 2 (2/0) | 43445 | 211 | 1955 | 11.9 |
| M1 | multihop | N | 1 | 2 (0/2) | 42792 | 227 | 5178 | 6.8 |
| M2 | multihop | C | 1 | 5 (5/0) | 94821 | 466 | 8588 | 17.4 |
| M2 | multihop | N | 0 | 1 (0/1) | 26674 | 156 | 1810 | 6.3 |
| R1 | read | C | 1 | 1 (1/0) | 28334 | 138 | 628 | 6.7 |
| R1 | read | N | 0 | 0 (0/0) | 13015 | 38 | 0 | 4.3 |
| R2 | read | C | 1 | 1 (1/0) | 28376 | 171 | 796 | 5.5 |
| R2 | read | N | 1 | 1 (0/1) | 27552 | 114 | 1396 | 5.4 |
| R3 | read | C | 1 | 1 (1/0) | 28331 | 177 | 416 | 12.3 |
| R3 | read | N | 1 | 1 (0/1) | 27995 | 137 | 6618 | 9.8 |
| S1 | structure | C | 1 | 1 (1/0) | 28549 | 218 | 1216 | 9.3 |
| S1 | structure | N | 1 | 1 (0/1) | 26572 | 235 | 1490 | 7.4 |
| S2 | structure | C | 1 | 1 (1/0) | 31131 | 327 | 10564 | 7.0 |
| S2 | structure | N | 1 | 1 (0/1) | 26304 | 298 | 502 | 13.6 |
| X1 | crossref | C | 1 | 4 (4/0) | 71961 | 496 | 958 | 28.6 |
| X1 | crossref | N | 1 | 3 (0/3) | 54667 | 279 | 3741 | 7.8 |
| X2 | crossref | C | 1 | 4 (4/0) | 74079 | 472 | 6639 | 23.9 |
| X2 | crossref | N | 1 | 1 (0/1) | 26485 | 104 | 1332 | 5.4 |

| kind | arm | n | correct | calls | in tok | bytes | C/N calls | C/N in tok | C/N bytes | S1 C/N calls | S1 C/N in | S1 C/N bytes |
|--|--|--|--|--|--|--|--|--|--|--|--|--|
| locate | N | 3 | 1.00 | 1.0 | 27235 | 1592 | | | | | | |
| locate | C | 3 | 1.00 | 1.0 | 28311 | 564 | 100% | 104% | 35% | 100% | 103% | 35% |
| read | N | 3 | 0.67 | 0.7 | 22854 | 2671 | | | | | | |
| read | C | 3 | 1.00 | 1.0 | 28347 | 613 | 150% | 124% | 23% | 60% | 76% | 17% |
| structure | N | 2 | 1.00 | 1.0 | 26438 | 996 | | | | | | |
| structure | C | 2 | 1.00 | 1.0 | 29840 | 5890 | 100% | 113% | 591% | 133% | 126% | 253% |
| crossref | N | 2 | 1.00 | 2.0 | 40576 | 2536 | | | | | | |
| crossref | C | 2 | 1.00 | 4.0 | 73020 | 3798 | 200% | 180% | 150% | 175% | 159% | 129% |
| multihop | N | 2 | 0.50 | 1.5 | 34733 | 3494 | | | | | | |
| multihop | C | 2 | 1.00 | 3.5 | 69133 | 5272 | 233% | 199% | 151% | 225% | 200% | 227% |

series2 overall N: correct 10/12 calls 1.17 in 29480 out 160 bytes 2237 wall 7.2
series2 overall C: correct 12/12 calls 1.92 in 42830 out 255 bytes 2788 wall 11.8
series2 C as % of N: calls 164% in 145% bytes 125%
series1 overall N: correct 11/12 calls 1.58 in 34783 out 181 bytes 2340 wall 7.4
series1 overall C: correct 11/12 calls 2.17 in 45066 out 310 bytes 2308 wall 9.5
series1 C as % of N: calls 137% in 130% bytes 99%

## Arm C commands (grouped by task; session flag omitted; full list in results/series2/tables.txt)
All 24 command lines exit 0 except four (below). Needed: every single-call task's one call answered it. Not needed: M2 `search symbol "Integer"` (bare/qualified `read type` resolves); M1/S1/S2 read type without search (correct). X1 and X2 wandered (below). No grep/sed/cat fallback anywhere (0 shell calls in arm C).
Devx errors verbatim (rc=1):
- X1 `devx callers "_factorint_small"`: `error: Call graph queries are not supported for Python symbol '_factorint_small'.`
- X1 `devx references "sympy.ntheory.factor_._factorint_small"`: `error: Symbol 'sympy.ntheory.factor_._factorint_small' was not found.`
- X2 `devx references "_symbol"`: `error: Call graph queries are not supported for Python symbol '_symbol'.` (I reproduced the text afterwards; the agent saw empty output).
`search symbol` before `read type`: 1 of 8 read-type calls (M2, once); series 1 searched before almost every one. `callers`/`references` used on both cross-ref tasks (X1 first call callers, X2 first call references), all four failed; both tasks then fell back to `search symbol`/`search text` and, for X2, `read file --range`.

## Where C still used more calls or bytes than N
- L1/L3 bytes: `search symbol` returns several candidate lines (383/1023 B) versus a targeted grep (105/53 B); calls equal.
- R1: N answered from memory with 0 calls and was wrong; C read the method (1 call, correct).
- M2: N 1 call and wrong; C walked Integer->Rational->Number->AtomicExpr (5 calls, correct).
- S2: `read type --full` on Sieve returned 10564 B versus 502 B for N's grep.
- X1: 4 calls vs 3; two were the failed callers/references attempts.
- X2: 4 vs 1; N grepped the call site directly; C's callers/references failed on Python.
- Input tokens are higher for C on every task with more calls; on one-call locate tasks C's input is 1k-2k tokens above N (L1 28279 vs 27164), consistent with the AGENTS.md block being loaded.

## Verdict
The shipped guidance removed the series-1 search-before-read-type pattern (1 of 8 vs near-always) and the structure losses on calls (S1/S2 100% of N calls vs 133%), and arm C scored 12/12 against N's 10/12 (series 1: 11/12 each). Overall C is still more expensive than N: calls 164% (series 1: 137%), input tokens 145% (130%), result bytes 125% (99%). N's totals are flattered by two zero/one-call wrong answers (R1, M2), so the ratios are not like for like; one rep per cell, no variance estimate. DevX cut result bytes at equal correctness on locate (35% of N), read (23% of N) and equal calls on locate, structure; read-kind call count rose to 150% only because N skipped reading on R1 and failed. Crossref (200%) and multihop (233%) remain the losses: the block advertises `callers`/`references`, but on Python they return "not supported", so the agent pays for the failed calls before falling back. Series-1 vs series-2 per-kind movement is in the table's last three columns; with n=2 per kind these are single-run comparisons.
