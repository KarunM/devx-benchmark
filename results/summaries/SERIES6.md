# Series 6: held-out 12 tasks on gpt-5.6-luna

Admitted to the evidence set (2026-10-12); see results/summaries/FACTS-benchmark.md

Model: `gpt-5.6-luna`, passed with `-m` to both arms (third probe answered "ok", rc 0; earlier probes `gpt-5` and `gpt-5-codex` were rejected for ChatGPT accounts). Reasoning effort: `medium`, from `codex_home*/config.toml` (unchanged). Same DevX binary as series 5 (`devx version` 1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04), same guidance, both arms read-only, 1 rep, 24 runs, all exit 0, none timed out. F2/F3 listings before and after are identical (only `.devx/` excluded). Correctness in the table is the automated scorer; verified correctness comes from an independent blinded rescore (`results/series6/rescore-blind6.csv`, joined with the out-of-repo key into `results/series6/rescore6.csv`). Blind pack: `results/series6/blind/`.

Verified correctness (blinded rescore, 24/24 answers): arm C 12/12, arm N 12/12. Series 5 verified (rescore.csv): C 10/12, N 10/12. Agreement between the automated scorer and the blinded rescore: 24/24 answers.

Maintainer note: A07 (H-M1, arm C) was checked by hand and judged correct, because it names CodePrinter at codeprinter.py:53 after walking the chain.

Rescorer's immaterial deviations (all rated correct): A21 (H-X1, arm C) wrong line numbers for sign/limitinf with correct names; A22 (H-R2, arm N) line 15 vs 16; A18 (H-R1, arm C) line 163 vs 164.

Verified both-correct comparison (n stated per line):
- S6 both-correct (verified) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S5 both-correct (verified, rescore.csv) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
- S5 all 12 (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)

Arm C had no devx errors (every devx command exited 0), no zero-tool-call runs and no grep/sed/cat/find fallbacks. Where C used more calls or bytes than N is listed below.

| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 25796 | 1762 | 15.4 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 22627 | 49 | 5.1 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 24561 | 982 | 7.4 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 22612 | 64 | 4.6 | 0 |
| H-R1 | C | 1 | 2 (2/0) | 37600 | 1150 | 13.9 | 0 |
| H-R1 | N | 1 | 3 (0/3) | 61295 | 1051628 | 7.6 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 24553 | 665 | 10.9 | 0 |
| H-S1 | N | 1 | 1 (0/1) | 24987 | 4542 | 5.7 | 0 |
| H-X1 | C | 1 | 3 (3/0) | 54015 | 4849 | 10.7 | 0 |
| H-X1 | N | 1 | 2 (0/2) | 37025 | 6548 | 13.1 | 0 |
| H-M1 | C | 1 | 3 (3/0) | 51849 | 5846 | 10.5 | 0 |
| H-M1 | N | 1 | 1 (0/1) | 22885 | 1031 | 5.6 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 25457 | 724 | 6.6 | 0 |
| H-L3 | N | 1 | 1 (0/1) | 22658 | 304 | 4.9 | 0 |
| H-R2 | C | 1 | 3 (3/0) | 51063 | 4641 | 9.7 | 0 |
| H-R2 | N | 1 | 2 (0/2) | 55921 | 65362 | 6.8 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 24588 | 1358 | 9.0 | 0 |
| H-R3 | N | 1 | 2 (0/2) | 41892 | 15848 | 12.4 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 24517 | 942 | 5.4 | 0 |
| H-S2 | N | 1 | 1 (0/1) | 22669 | 313 | 9.0 | 0 |
| H-X2 | C | 1 | 2 (2/0) | 43242 | 13722 | 10.6 | 0 |
| H-X2 | N | 1 | 3 (0/3) | 51323 | 7778 | 10.9 | 0 |
| H-M2 | C | 1 | 3 (3/0) | 51634 | 5449 | 8.7 | 0 |
| H-M2 | N | 1 | 2 (0/2) | 37151 | 14131 | 7.1 | 0 |

Arm C automated correct: 12/12 (automated)
Arm N automated correct: 12/12 (automated)

S6 both-correct (automated) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S5 both-correct (automated, recomputed) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
S5 all 12 (recomputed) (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
S5 arm correctness (automated): C 11/12, N 10/12
S6 arm correctness (automated): C 12/12, N 12/12

Zero-tool-call runs: none
C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1762 vs N 49
- H-L2: calls C 1 vs N 1; bytes C 982 vs N 64
- H-X1: calls C 3 vs N 2; bytes C 4849 vs N 6548
- H-M1: calls C 3 vs N 1; bytes C 5846 vs N 1031
- H-L3: calls C 1 vs N 1; bytes C 724 vs N 304
- H-R2: calls C 3 vs N 2; bytes C 4641 vs N 65362
- H-S2: calls C 1 vs N 1; bytes C 942 vs N 313
- H-X2: calls C 2 vs N 3; bytes C 13722 vs N 7778
- H-M2: calls C 3 vs N 2; bytes C 5449 vs N 14131

Arm C grep/sed/cat/find fallbacks and devx non-zero exits (command, exit):
