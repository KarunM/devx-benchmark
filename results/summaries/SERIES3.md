# Series 3: 12 tasks x arms C and N, 1 rep, gpt-6-luna, CS25 build 1.6.14+2f2c19d, arm C guided only by DevX's regenerated AGENTS.md block

Setup: published bin/2f2c19d/, clibin/devx repointed; `devx version` = 1.6.14+2f2c19d544f9323763e5f32cc5f8f48b72be8d8b (seen before runs); index Current, 1605 files, no reindex. Shipped block = 3030 bytes; single edit (`SESSION_ID=$(devx session create ...)` line replaced by `SESSION_ID=af688c1a-...`) gives 2990 bytes in codex_home_c/AGENTS.md; `grep -c` "callers" 1, "Bare or" 1, literal "--full only" 0 (text reads "use `--full` only when you need bodies"). Arm C: reduced preamble, workspace-write; arm N: unchanged, read-only. Exactly 24 paid runs, no reruns, all rc=0. F2 listing (excluding .devx) before/after: no differences.

## 1. Per run
| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |
|--|--|--|--|--|--|--|--|--|
| L1 | locate | C | 1 | 1 (1/0) | 29336 | 123 | 383 | 5.6 |
| L1 | locate | N | 1 | 1 (0/1) | 26163 | 116 | 105 | 5.7 |
| L2 | locate | C | 1 | 1 (1/0) | 28278 | 121 | 287 | 9.4 |
| L2 | locate | N | 1 | 1 (0/1) | 27269 | 87 | 4617 | 4.8 |
| L3 | locate | C | 1 | 1 (1/0) | 28466 | 119 | 1023 | 7.1 |
| L3 | locate | N | 1 | 1 (0/1) | 26139 | 117 | 53 | 5.1 |
| M1 | multihop | C | 0 | 3 (3/0) | 59622 | 274 | 6644 | 12.6 |
| M1 | multihop | N | 1 | 2 (0/2) | 40014 | 242 | 1155 | 8.4 |
| M2 | multihop | C | 1 | 4 (4/0) | 79190 | 420 | 7557 | 28.1 |
| M2 | multihop | N | 0 | 1 (0/1) | 26705 | 177 | 1810 | 5.7 |
| R1 | read | C | 1 | 1 (1/0) | 28393 | 176 | 628 | 6.3 |
| R1 | read | N | 1 | 2 (0/2) | 46647 | 146 | 17322 | 7.1 |
| R2 | read | C | 1 | 1 (1/0) | 28442 | 167 | 867 | 16.6 |
| R2 | read | N | 1 | 1 (0/1) | 26447 | 153 | 1164 | 35.6 |
| R3 | read | C | 1 | 1 (1/0) | 28343 | 151 | 349 | 6.1 |
| R3 | read | N | 1 | 1 (0/1) | 29438 | 134 | 8351 | 7.0 |
| S1 | structure | C | 1 | 1 (1/0) | 28625 | 255 | 1216 | 9.1 |
| S1 | structure | N | 1 | 1 (0/1) | 26572 | 201 | 1490 | 6.6 |
| S2 | structure | C | 1 | 1 (1/0) | 28472 | 212 | 728 | 6.4 |
| S2 | structure | N | 1 | 1 (0/1) | 26303 | 320 | 502 | 6.5 |
| X1 | crossref | C | 1 | 1 (1/0) | 28356 | 157 | 384 | 6.3 |
| X1 | crossref | N | 0 | 1 (0/1) | 26184 | 184 | 202 | 8.4 |
| X2 | crossref | C | 1 | 2 (2/0) | 43945 | 297 | 5351 | 9.3 |
| X2 | crossref | N | 1 | 1 (0/1) | 26486 | 103 | 1332 | 6.7 |

## 2. Per kind, C as % of N (S3 / S2 / S1) and mean correct (C / N)
| kind | C/N calls S3/S2/S1 | C/N in tok S3/S2/S1 | C/N bytes S3/S2/S1 | correct C N (S3) | (S2) | (S1) |
|--|--|--|--|--|--|--|
| locate | 100% / 100% / 100% | 108% / 104% / 103% | 35% / 35% / 35% | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| read | 75% / 150% / 60% | 83% / 124% / 76% | 7% / 23% / 17% | 1.00 / 1.00 | 1.00 / 0.67 | 1.00 / 1.00 |
| structure | 100% / 100% / 133% | 108% / 113% / 126% | 98% / 591% / 253% | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| crossref | 150% / 200% / 175% | 137% / 180% / 159% | 374% / 150% / 129% | 1.00 / 0.50 | 1.00 / 1.00 | 0.50 / 1.00 |
| multihop | 233% / 233% / 225% | 208% / 199% / 200% | 479% / 151% / 227% | 0.50 / 0.50 | 1.00 / 0.50 | 1.00 / 0.50 |


## 3. Overall
- series3 N: correct 10/12 calls 1.17 in 29531 bytes 3175 wall 9.0
- series3 C: correct 11/12 calls 1.50 in 36622 bytes 2118 wall 10.2
- series3 C%N all12: calls/in/bytes 129% / 124% / 67%
- series3 both-correct n=9 (L1,L2,L3,R1,R2,R3,S1,S2,X2): calls/in/bytes 100% / 104% / 31%
- series2 N: correct 10/12 calls 1.17 in 29480 bytes 2237 wall 7.2
- series2 C: correct 12/12 calls 1.92 in 42830 bytes 2788 wall 11.8
- series2 C%N all12: calls/in/bytes 164% / 145% / 125%
- series2 both-correct n=10 (L1,L2,L3,M1,R2,R3,S1,S2,X1,X2): calls/in/bytes 131% / 124% / 97%
- series1 N: correct 11/12 calls 1.58 in 34783 bytes 2340 wall 7.4
- series1 C: correct 11/12 calls 2.17 in 45066 bytes 2308 wall 9.5
- series1 C%N all12: calls/in/bytes 137% / 130% / 99%
- series1 both-correct n=10 (L1,L2,L3,M1,R1,R2,R3,S1,S2,X1): calls/in/bytes 94% / 99% / 48%

Series 3 both-correct line: 9 tasks qualify (M1 C wrong; M2 and X1 N wrong): calls 100%, input tokens 104%, result bytes 31% (S2 maintainer figures 131/124/97 over 10 tasks; S1 94/99/48 over 10).

## 4. Arm C commands (full list results/series3/tables.txt)
Single-call tasks: L1 `search symbol factorint` 383 B; L2 `search symbol uniquely_named_symbol` 287 B; L3 `search symbol Rational` 1023 B; R1 `read method sympy.core.symbol.Dummy.__new__` 628 B; R2 `search symbol Symbol._sanitize` 867 B; R3 `read method sympy.core.symbol.Wild.__new__` 349 B; S1 `read type Symbol` 1216 B; S2 `read type Sieve` 728 B; X1 `callers _factorint_small` 384 B. All rc=0 and all needed. Multi-call: M1 `read type Symbol` 1216, `search symbol Boolean` 1155, `read type Boolean --full` 4273 (rc 0; last two avoidable; wrong answer, see below); M2 `read type` Integer 2410, Rational 2424, Number 1985, AtomicExpr 738 (rc 0; correct); X2 `callers "_symbol"` 428 B rc=2, then `callers "sympy.core.symbol.<module>._symbol"` 4923 B rc=0 (the second was needed).
Counts: `search symbol` before `read type`: 1 of 8 read-type calls (M1; series 2: 1 of 8). `callers`/`references` on X1/X2: 3 calls (X1 1, X2 2), 2 succeeded with hits, 1 returned the ambiguity candidate list (rc=2, first line `ambiguous: _symbol matches 3 symbols`). `--full`: 1 (M1). grep/sed/cat fallbacks: 0. Devx rc=1 errors: none (series 2 had 3).

## 5. Where C still used more calls or bytes than N
- L1, L3: one search call either way; C returned more bytes (383 vs 105, 1023 vs 53) because N's grep was narrower.
- M1: C wrong; it read Boolean with `--full` (no per-line numbers in the output) and answered `to_nnf` at boolalg.py:118, expected :131; N did 2 greps.
- M2: N answered in 1 call but was wrong (0); C's 4 `read type` calls climbed the hierarchy and were right.
- S2: 728 vs 502 B, same call count (S2 was 10564 B in series 2).
- X1: equal calls; C 384 vs 202 B. N answered with only `factorint` and missed `_perfect_power` (wrong).
- X2: C needed 2 calls and 5351 B (ambiguous bare name, then the 44-site list) vs N 1 call, 1332 B; both correct.
- R2: C smaller in bytes, equal calls.

## 6. Verdict
Python `callers`/`references` removed the cross-ref loss on call count: X1 went from 4 calls (series 2) to 1, X2 from 4 to 2, and X1 is now right where N is wrong. They did not remove it on bytes in X2 (5351 B vs N's 1332 B) because the bare name is ambiguous and the qualified list is 4.9 KB. Multihop is still the weak kind: M1 and M2 cost C 3 and 4 calls vs 2 and 1 (233% calls, 208% input tokens), and M1 was answered wrongly from a `--full` read. Overall C was 11/12 vs N 10/12 correct, with calls 129%, input tokens 124%, result bytes 67% of N; over the 9 tasks both got right, 100% calls, 104% tokens, 31% bytes. DevX cuts context where grep returns wide output (R1 628 vs 17322 B, R3 349 vs 8351 B, L2 287 vs 4617 B) and cuts calls only on cross-ref (X1); locate and structure tasks are a tie on calls with about 8% more input tokens (guidance preamble). Across series 1 to 3 the same task changed correctness in both arms (N: R1 0 in S2, X1 0 in S3; C: M1 0 in S3, X1/X2 0.5 in S1) and individual rows moved by 2 to 10x in bytes, so n=1 differences of one call or one task are noise; 3 reps are worth running, since every cross-arm gap smaller than about one task and all the multihop/crossref figures flip between series.
