# SERIES4 - 3-rep run, CS26 build (1.6.14+04a02ef), 12 tasks x arms C and N x 3 reps (72 paid Codex runs, gpt-6-luna)

Arm C: clibin PATH (04a02ef build), `codex_home_c/AGENTS.md` (3,001 B, regenerated, one edit: session id), reduced preamble, workspace-write. Arm N: grep/sed/cat, read-only. Series 1 to 3 were n=1. All 72 rows have exit 0, none timed out. F2 file listing before/after identical (only `.devx/` excluded). Raw data: `results/series4/rows.csv`, `tables.txt` (all C commands).

## 1. Per task (medians over 3 reps)
| task | kind | arm | correct | med calls | med in tok | med bytes | bytes min-max | med wall s |
|--|--|--|--|--|--|--|--|--|
| L1 | locate | C | 3/3 | 1 | 28368 | 383 | 383-383 | 5.2 |
| L1 | locate | N | 3/3 | 1 | 26178 | 105 | 105-105 | 6.8 |
| L2 | locate | C | 3/3 | 1 | 28297 | 287 | 287-287 | 7.7 |
| L2 | locate | N | 3/3 | 1 | 27421 | 5810 | 4617-18679 | 5.7 |
| L3 | locate | C | 3/3 | 1 | 28490 | 1023 | 1023-1023 | 6.7 |
| L3 | locate | N | 3/3 | 1 | 26114 | 53 | 53-53 | 7.8 |
| M1 | multihop | C | 3/3 | 2 | 43649 | 2080 | 1542-2080 | 11.8 |
| M1 | multihop | N | 3/3 | 1 | 27695 | 4233 | 628-6169 | 7.9 |
| M2 | multihop | C | 3/3 | 4 | 77569 | 7989 | 6958-7989 | 12.9 |
| M2 | multihop | N | 1/3 | 1 | 26690 | 1810 | 1786-1810 | 7.3 |
| R1 | read | C | 3/3 | 1 | 28399 | 628 | 628-696 | 8.0 |
| R1 | read | N | 3/3 | 1 | 28268 | 3370 | 1081-6843 | 6.8 |
| R2 | read | C | 3/3 | 1 | 28470 | 867 | 867-867 | 15.5 |
| R2 | read | N | 3/3 | 1 | 26559 | 1336 | 1073-1436 | 6.6 |
| R3 | read | C | 3/3 | 1 | 28386 | 416 | 416-416 | 12.2 |
| R3 | read | N | 3/3 | 1 | 28354 | 7843 | 6618-7843 | 6.1 |
| S1 | structure | C | 3/3 | 1 | 28639 | 1302 | 1302-1302 | 10.0 |
| S1 | structure | N | 3/3 | 1 | 27579 | 1490 | 1490-10067 | 7.1 |
| S2 | structure | C | 3/3 | 1 | 28484 | 728 | 728-1605 | 5.8 |
| S2 | structure | N | 3/3 | 1 | 26304 | 502 | 224-502 | 7.7 |
| X1 | crossref | C | 3/3 | 1 | 28390 | 384 | 384-384 | 6.7 |
| X1 | crossref | N | 2/3 | 2 | 40468 | 2776 | 202-3241 | 9.6 |
| X2 | crossref | C | 3/3 | 2 | 43152 | 4923 | 1496-5351 | 7.8 |
| X2 | crossref | N | 3/3 | 1 | 26480 | 1332 | 1332-1332 | 6.2 |

## 2. Per kind (mean of per-task medians) and C as % of N, beside series 3, 2, 1 (n=1 each)
| kind | arm | calls | in tok | bytes | correct | C%N calls/in/bytes S4 | S3 | S2 | S1 |
|--|--|--|--|--|--|--|--|--|--|
| locate | N | 1.00 | 26571 | 1989 | 9/9 |  | | | |
| locate | C | 1.00 | 28385 | 564 | 9/9 | 100% / 107% / 28% | 100% / 108% / 35% | 100% / 104% / 35% | 100% / 103% / 35% |
| read | N | 1.00 | 27727 | 4183 | 9/9 |  | | | |
| read | C | 1.00 | 28418 | 637 | 9/9 | 100% / 102% / 15% | 75% / 83% / 7% | 150% / 124% / 23% | 60% / 76% / 17% |
| structure | N | 1.00 | 26942 | 996 | 6/6 |  | | | |
| structure | C | 1.00 | 28562 | 1015 | 6/6 | 100% / 106% / 102% | 100% / 108% / 98% | 100% / 113% / 591% | 133% / 126% / 253% |
| crossref | N | 1.50 | 33474 | 2054 | 5/6 |  | | | |
| crossref | C | 1.50 | 35771 | 2654 | 6/6 | 100% / 107% / 129% | 150% / 137% / 374% | 200% / 180% / 150% | 175% / 159% / 129% |
| multihop | N | 1.00 | 27192 | 3022 | 4/6 |  | | | |
| multihop | C | 3.00 | 60609 | 5034 | 6/6 | 300% / 223% / 167% | 233% / 208% / 479% | 233% / 199% / 151% | 225% / 200% / 227% |
| ALL | N | 1.08 | 28176 | 2555 | 33/36 |  | | | |
| ALL | C | 1.42 | 35024 | 1751 | 36/36 | 131% / 124% / 69% | 129% / 124% / 67% | 164% / 145% / 125% | 137% / 130% / 99% |

## 3. Overall
- Correctness: C 36/36, N 33/36 (N misses: M2 twice, X1 once).
- C as % of N on medians over all 12 tasks: calls 131%, input tokens 124%, result bytes 69% (C 1.42 / 35,024 / 1,751 vs N 1.08 / 28,176 / 2,555).
- Both-correct in ALL 3 reps: n=10 (L1,L2,L3,M1,R1,R2,R3,S1,S2,X2): calls 120%, input 116%, bytes 48% of N.
- Both-correct in the majority of reps: n=11 (adds X1): calls 108%, input 110%, bytes 45%.

## 4. Stability
L1 C: correct [1, 1, 1] stable bytes 383-383 | N: correct [1, 1, 1] stable bytes 105-105
L2 C: correct [1, 1, 1] stable bytes 287-287 | N: correct [1, 1, 1] stable bytes 4617-18679
L3 C: correct [1, 1, 1] stable bytes 1023-1023 | N: correct [1, 1, 1] stable bytes 53-53
M1 C: correct [1, 1, 1] stable bytes 1542-2080 | N: correct [1, 1, 1] stable bytes 628-6169
M2 C: correct [1, 1, 1] stable bytes 6958-7989 | N: correct [0, 0, 1] FLIP bytes 1786-1810
R1 C: correct [1, 1, 1] stable bytes 628-696 | N: correct [1, 1, 1] stable bytes 1081-6843
R2 C: correct [1, 1, 1] stable bytes 867-867 | N: correct [1, 1, 1] stable bytes 1073-1436
R3 C: correct [1, 1, 1] stable bytes 416-416 | N: correct [1, 1, 1] stable bytes 6618-7843
S1 C: correct [1, 1, 1] stable bytes 1302-1302 | N: correct [1, 1, 1] stable bytes 1490-10067
S2 C: correct [1, 1, 1] stable bytes 728-1605 | N: correct [1, 1, 1] stable bytes 224-502
X1 C: correct [1, 1, 1] stable bytes 384-384 | N: correct [1, 0, 1] FLIP bytes 202-3241
X2 C: correct [1, 1, 1] stable bytes 1496-5351 | N: correct [1, 1, 1] stable bytes 1332-1332
stable cells (no correctness flip): 22 of 24

Correctness was stable in 22 of 24 (task, arm) cells; flips: N on M2 ([0,0,1]) and N on X1 ([1,0,1]). C never flipped. Bytes ranges: C is exactly constant in 7 of 12 tasks (L1, L2, L3, R2, R3, S1, X1); N varies widely where output is grep-dependent (L2 4,617-18,679; S1 1,490-10,067; R1 1,081-6,843; M1 628-6,169).

## 5. Arm C commands (36 runs, 0 with no devx call)
- `search symbol` immediately before `read type`: 3 pairs (M2 reps 2 and 3: `search symbol "Integer"`; S2 once: `search symbol "Sieve"`). M1 reps 1 and 3 ran `read type Symbol` first, then `search symbol to_nnf`.
- `read type` total 18. Hierarchy walks (consecutive `read type`): 3, all M2, each length 3 (Integer, Rational, Number), one per rep, no search between levels.
- `callers`: 8 calls, 6 succeeded; `references`: 0 uses.
- `--full`: 3 uses, all X2 (reps 1 and 3); in rep 3 the bare-name `callers "_symbol" --full` failed first.
- grep/sed/cat fallbacks: 0.
- devx errors (both X2, rc=2, 428 B): `devx callers "_symbol"` -> "ambiguous: _symbol matches 3 symbols / sympy.core.symbol.<module>._symbol  sympy/core/symbol.py:64-128  Method / functions.elementary.miscellaneous.IdentityFunction._symbol ..." (rep 2 without flag, rep 3 with `--full`). Each cost one extra call and the agent then used the qualified name.

## 6. Tasks where C's median calls or bytes exceed N's
- L1, L3 (bytes 383 vs 105, 1,023 vs 53): N's grep matched one line; `search symbol` returns the declaration plus neighbours.
- S2 (bytes 728 vs 502): same, outline larger than a targeted grep.
- M1 (2 vs 1 call, but bytes 2,080 vs 4,233): C did `read type Symbol` then `search symbol to_nnf`; N's single grep sometimes landed directly (N bytes 628-6,169).
- M2 (4 vs 1 call, 7,989 vs 1,810 B): C walked Integer, Rational, Number with three 2.0-2.5 KB `read type` outlines plus a search; N's single grep on `class` lines answered it but was correct only 1 of 3 reps.
- X2 (2 vs 1 call, 4,923 vs 1,332 B): bare `_symbol` is ambiguous (3 matches), so a failed/ambiguous call then the qualified list of 44 sites (4,923 B with `--full`, 1,068 B grouped); N's grep was a single narrow match.

## 7. Verdict
DevX cut context at equal correctness where grep output is wide: read tasks (bytes 15% of N, 637 vs 4,183 B; R3 416 vs 7,843 B), locate tasks (28%, 564 vs 1,989 B, driven by L2 287 vs 5,810 B), at 100% calls and about 102-107% input tokens (the guidance preamble). Crossref was a call tie (1.5 vs 1.5) at 107% tokens and 129% bytes, but C was 3/3 on X1 where N was 2/3 and C needed 1 call against N's 2. Structure was a tie on calls (100%) and bytes (102%). It does not cut calls or context on multihop: C 3.0 vs N 1.0 median calls, 223% input tokens, 167% bytes, because the hierarchy walk costs one read per level; but C was 6/6 correct against N's 4/6 (M2 N 1/3), and N's single-call answers there were mostly wrong. Overall C 131% calls, 124% input tokens, 69% bytes; on the 10 all-reps-both-correct tasks 120% / 116% / 48%. Net: fewer bytes, more calls and tokens, higher correctness in this sample. Input tokens are dominated by a ~26K fixed prompt, so byte savings barely move token totals.

Reviewer pushback: (1) sandbox asymmetry, C ran workspace-write, N read-only; (2) n=3 per cell, correctness differences are 3 runs of 36 (N M2 x2, X1 x1), not significant; (3) one fixture (sympy), 12 tasks, tasks written by us with fixed expected strings; (4) one model (gpt-6-luna); (5) `callers` is text-backed and name-based, not a resolved call graph (44 sites over 23 functions for `_symbol` incl. docstring examples), ambiguity on bare names costs a call; (6) C is told by its guidance which commands to use and not to use grep, N has no instruction beyond tools; (7) the guidance was edited between series and tuned on these same tasks. No advocacy intended.
