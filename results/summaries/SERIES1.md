# Series 1: 12 tasks x arms C (devx CLI) and N (shell), 1 rep, gpt-6-luna, CS23 build 1.6.14+33b9ddf

Setup: `devx version` = 1.6.14+33b9ddfc46911630e7b2eb62dca6367b2376d40e (seen before runs); `devx index status` Current, 1605 files, no reindex; `read type sympy.core.symbol.Symbol` = 1216 bytes; `search text "def subs"` works (agent output, 17 more hits truncated, coverage line says 1 indexed path not searchable). Asymmetry: arm C ran `workspace-write`, arm N `read-only`. F2 before/after listing: only `.devx/devx.db` changed. 24 paid runs, no reruns, all rc=0, no timeouts, no stderr errors. Pairs alternated C,N / N,C.

## Tables
| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |
|--|--|--|--|--|--|--|--|--|
| L1 | locate | C | 1 | 1 (1/0) | 28081 | 166 | 383 | 9.3 |
| L1 | locate | N | 1 | 1 (0/1) | 26155 | 103 | 105 | 5.4 |
| L2 | locate | C | 1 | 1 (1/0) | 27019 | 154 | 287 | 5.9 |
| L2 | locate | N | 1 | 1 (0/1) | 27416 | 88 | 4617 | 7.2 |
| L3 | locate | C | 1 | 1 (1/0) | 27209 | 149 | 1023 | 8.4 |
| L3 | locate | N | 1 | 1 (0/1) | 26114 | 92 | 53 | 5.3 |
| M1 | multihop | C | 1 | 4 (4/0) | 71661 | 462 | 4310 | 10.7 |
| M1 | multihop | N | 1 | 2 (0/2) | 41610 | 249 | 4515 | 8.6 |
| M2 | multihop | C | 1 | 5 (5/0) | 91484 | 593 | 8694 | 14.6 |
| M2 | multihop | N | 0 | 2 (0/2) | 39847 | 242 | 1210 | 8.8 |
| R1 | read-and-answer | C | 1 | 1 (1/0) | 27128 | 170 | 628 | 8.7 |
| R1 | read-and-answer | N | 1 | 2 (0/2) | 39852 | 161 | 1533 | 6.5 |
| R2 | read-and-answer | C | 1 | 1 (1/0) | 27200 | 238 | 796 | 5.9 |
| R2 | read-and-answer | N | 1 | 2 (0/2) | 39869 | 162 | 2230 | 8.9 |
| R3 | read-and-answer | C | 1 | 1 (1/0) | 27041 | 144 | 349 | 5.4 |
| R3 | read-and-answer | N | 1 | 1 (0/1) | 27996 | 149 | 6618 | 8.0 |
| S1 | structure | C | 1 | 2 (2/0) | 41627 | 287 | 2377 | 8.4 |
| S1 | structure | N | 1 | 2 (0/2) | 39822 | 257 | 1075 | 7.3 |
| S2 | structure | C | 1 | 2 (2/0) | 41437 | 328 | 1605 | 10.8 |
| S2 | structure | N | 1 | 1 (0/1) | 26303 | 231 | 502 | 6.2 |
| X1 | crossref | C | 1 | 1 (1/0) | 27096 | 143 | 543 | 5.7 |
| X1 | crossref | N | 1 | 3 (0/3) | 54921 | 333 | 4289 | 9.4 |
| X2 | crossref | C | 0 | 6 (6/0) | 103806 | 884 | 6703 | 20.2 |
| X2 | crossref | N | 1 | 1 (0/1) | 27492 | 103 | 1332 | 7.6 |

| kind | arm | n | correct | calls | in tok | bytes | C/N calls | C/N in tok | C/N bytes |
|--|--|--|--|--|--|--|--|--|--|
| locate | N | 3 | 1.00 | 1.0 | 26562 | 1592 | | | |
| locate | C | 3 | 1.00 | 1.0 | 27436 | 564 | 100% | 103% | 35% |
| read | N | 3 | 1.00 | 1.7 | 35906 | 3460 | | | |
| read | C | 3 | 1.00 | 1.0 | 27123 | 591 | 60% | 76% | 17% |
| structure | N | 2 | 1.00 | 1.5 | 33062 | 788 | | | |
| structure | C | 2 | 1.00 | 2.0 | 41532 | 1991 | 133% | 126% | 253% |
| crossref | N | 2 | 1.00 | 2.0 | 41206 | 2810 | | | |
| crossref | C | 2 | 0.50 | 3.5 | 65451 | 3623 | 175% | 159% | 129% |
| multihop | N | 2 | 0.50 | 2.0 | 40728 | 2862 | | | |
| multihop | C | 2 | 1.00 | 4.5 | 81572 | 6502 | 225% | 200% | 227% |
overall N: correct 11/12 calls 1.58 in 34783 bytes 2340 wall 7.4
overall C: correct 11/12 calls 2.17 in 45066 bytes 2308 wall 9.5
C as % of N: calls 137% in 130% bytes 99%

## Arm C commands (all exit 0, no grep/sed fallback, no devx error)
Needed vs not: every `read`/`search` below was the answering call except: M1 `search symbol Symbol` and `search symbol Boolean` (resolved names, then read; Boolean never read), M2 `search symbol Integer` and `search symbol AtomicExpr` (walking the chain one class at a time), S1 `search symbol Symbol` (name resolution before read), S2 `search symbol Sieve`, X2 all six (wandering; final answer wrong). L1-L3, R1-R3, X1 single call, needed.
## L1
- 'devx search symbol "factorint" --session <SESSION-F2> --format agent' | 383 B | rc=0
## L2
- 'devx search symbol "uniquely_named_symbol" --session <SESSION-F2> --format agent' | 287 B | rc=0
## L3
- 'devx search symbol "Rational" --session <SESSION-F2> --format agent' | 1023 B | rc=0
## M1
- 'devx search symbol "Symbol" --session <SESSION-F2> --format agent' | 1161 B | rc=0
- 'devx read type "sympy.core.symbol.Symbol" --session <SESSION-F2> --format agent' | 1216 B | rc=0
- 'devx search symbol "Boolean" --session <SESSION-F2> --format agent' | 1155 B | rc=0
- 'devx search symbol "to_nnf" --session <SESSION-F2> --format agent' | 778 B | rc=0
## M2
- 'devx search symbol "Integer" --session <SESSION-F2> --format agent' | 1031 B | rc=0
- 'devx read type "sympy.core.numbers.Integer" --session <SESSION-F2> --format agent' | 2410 B | rc=0
- 'devx read type "sympy.core.numbers.Rational" --session <SESSION-F2> --format agent' | 2424 B | rc=0
- 'devx read type "sympy.core.numbers.Number" --session <SESSION-F2> --format agent' | 1985 B | rc=0
- 'devx search symbol "AtomicExpr" --session <SESSION-F2> --format agent' | 844 B | rc=0
## R1
- 'devx read method "sympy.core.symbol.Dummy.__new__" --session <SESSION-F2> --format agent' | 628 B | rc=0
## R2
- 'devx read method "sympy.core.symbol.Symbol._sanitize" --session <SESSION-F2> --format agent' | 796 B | rc=0
## R3
- 'devx read method "sympy.core.symbol.Wild.__new__" --session <SESSION-F2> --format agent' | 349 B | rc=0
## S1
- 'devx search symbol "Symbol" --session <SESSION-F2> --format agent' | 1161 B | rc=0
- 'devx read type "sympy.core.symbol.Symbol" --session <SESSION-F2> --format agent' | 1216 B | rc=0
## S2
- 'devx search symbol "Sieve" --session <SESSION-F2> --format agent' | 877 B | rc=0
- 'devx read type "sympy.ntheory.generate.Sieve" --session <SESSION-F2> --format agent' | 728 B | rc=0
## X1
- 'devx search text "_factorint_small" --session <SESSION-F2> --format agent' | 543 B | rc=0
## X2
- 'devx search text "_symbol(" --session <SESSION-F2> --format agent' | 1301 B | rc=0
- 'devx search text "_symbol(" "return _symbol" --session <SESSION-F2> --format agent' | 134 B | rc=0
- 'devx read type "sympy.core.symbol.Symbol" --session <SESSION-F2> --format agent' | 1216 B | rc=0
- 'devx search text "_symbol" --session <SESSION-F2> --format agent' | 2303 B | rc=0
- 'devx read method "sympy.core.symbol.<module>._symbol" --session <SESSION-F2> --format agent' | 1701 B | rc=0
- 'devx search symbol "sympy.core.symbol.symbols" --session <SESSION-F2> --format agent' | 48 B | rc=0

## C used more calls or bytes than N
- L1, L3: single grep; N output 105 and 53 bytes, `search symbol` returned 383 and 1023 bytes. No saving possible. L2 C bytes lower (grep hit 4617 B).
- S1, S2: C needed `search symbol` before `read type` (2 calls vs N 2 and 1); S1 outline 1216 B plus search 1161 B beats a one-line grep.
- M1: 4 calls (two symbol searches, one type read, one more search) vs N 2 greps.
- M2: walked the inheritance chain with 3 type reads of 2-2.4 KB each and 2 searches; N used 2 greps but answered `Expr` (wrong).
- X2: C chose search text then a wrong target (`symbols`), 6 calls, wrong; N grep found `uniquely_named_symbol` in 1 call.

## Verdict
Equal correctness overall (11/12 both). C wins on read-and-answer: 60% of N calls, 76% input tokens, 17% result bytes, same correctness, because `read method` returns just the body. X1 crossref also won (1 call vs 3, 543 B vs 4289 B). Locate ties on calls (1 vs 1), costs +3% input tokens, but 35% of N bytes on average (noise: 105 vs 383, 53 vs 1023, 4617 vs 287). C loses on structure (133% calls, 253% bytes), multihop (225% calls, 227% bytes; C 2/2 correct vs N 1/2) and the other crossref task X2 (wrong). Overall C = 137% of N calls, 130% input tokens, 99% result bytes, wall 9.5 s vs 7.4 s. C does not cut calls or context overall; the saving is confined to method reads and one crossref. One rep, n=2-3 per kind: indicative only.
