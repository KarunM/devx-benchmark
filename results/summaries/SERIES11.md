# Series 11: held-out 12 tasks on Codex CLI, model `gpt-6-sol`

Admitted to the evidence set (maintainer decision 2026-10-12); see FACTS.md F-FM-*.

Model ids: `gpt-6.1-sol` REJECTED: `{"type":"invalid_request_error","message":"The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account."}` (status 400). `gpt-6-sol` accepted (answered "ok", rc 0); rows.csv model column = gpt-6-sol on all 24 rows. Harness `run_bench.py` unchanged: `python3 run_bench.py --series series11 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1 --model gpt-6-sol` (series 6 with the model swapped); codex exec read-only, CODEX_HOME codex_home (N) / codex_home_c (C), Codex CLI 0.155.1. Reasoning effort: medium (probe header, from codex config). devx 1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04. Fixture listings: run_bench.py does not write them; results/f2-after-series11.txt and f3-after-series11.txt were taken after the series and are identical to the series-10 before and after listings (fixtures unchanged, .devx/ excluded). 1 rep, 24 runs, all exit 0.

Probes across this series: 4 (opus x2, gpt-6.1-sol, gpt-6-sol), one over the budget of 3 because the first Opus probe output was cut before the answer text. Blind pack: results/series11/blind/; key kept outside the repository (blind11-key/key.csv). Correctness is the automated scorer, see Verified results below.

| task | arm | auto correct | calls (devx/other) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 28707 | 1762 | 15.4 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 26809 | 707 | 7.7 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 28458 | 982 | 6.3 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 26536 | 64 | 5.7 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 28501 | 1078 | 9.5 | 0 |
| H-R1 | N | 1 | 2 (0/2) | 40434 | 1224 | 10.2 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 28350 | 468 | 10.3 | 0 |
| H-S1 | N | 1 | 2 (0/2) | 41007 | 3423 | 8.1 | 0 |
| H-X1 | C | 1 | 3 (3/0) | 59432 | 4263 | 16.5 | 0 |
| H-X1 | N | 1 | 3 (0/3) | 55560 | 2952 | 10.8 | 0 |
| H-M1 | C | 1 | 3 (3/0) | 59395 | 5846 | 12.1 | 0 |
| H-M1 | N | 1 | 1 (0/1) | 27647 | 185 | 9.4 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 29358 | 724 | 11.1 | 0 |
| H-L3 | N | 1 | 1 (0/1) | 26555 | 304 | 6.8 | 0 |
| H-R2 | C | 1 | 1 (1/0) | 28869 | 3581 | 9.0 | 0 |
| H-R2 | N | 1 | 2 (0/2) | 50730 | 19664 | 7.9 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 28485 | 1358 | 6.3 | 0 |
| H-R3 | N | 1 | 1 (0/1) | 29746 | 24461 | 9.5 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 28431 | 942 | 7.1 | 0 |
| H-S2 | N | 1 | 2 (0/2) | 41086 | 4947 | 12.2 | 0 |
| H-X2 | C | 1 | 4 (4/0) | 73180 | 3415 | 13.2 | 0 |
| H-X2 | N | 1 | 2 (0/2) | 41406 | 6109 | 8.6 | 0 |
| H-M2 | C | 1 | 2 (2/0) | 43869 | 3875 | 8.4 | 0 |
| H-M2 | N | 1 | 2 (0/2) | 42895 | 12567 | 8.0 | 0 |

Arm C correct: automated 12/12 (see Verified results below)
Arm N correct: automated 12/12 (see Verified results below)

- S11 both-correct (automated) (n=12): calls C 20 vs N 20 (100% of N); input tokens C 465035 vs N 450411 (103%); result bytes C 28294 vs N 76607 (37%)
- S11 all 12 (automated) (n=12): calls C 20 vs N 20 (100% of N); input tokens C 465035 vs N 450411 (103%); result bytes C 28294 vs N 76607 (37%)

Verified earlier series, recomputed from rows.csv + rescore files:
- S5 both-correct (VERIFIED) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
- S5 all 12 (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
- S6 both-correct (VERIFIED) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S7 both-correct (VERIFIED) (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S7 all 12 (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S8 both-correct (VERIFIED) (n=11): calls C 16 vs N 18 (89% of N); input tokens C 539293 vs N 537944 (100%); result bytes C 22630 vs N 14550 (156%)
- S8 all 12 (n=12): calls C 18 vs N 19 (95% of N); input tokens C 599063 vs N 574979 (104%); result bytes C 23553 vs N 14734 (160%)
- S9 both-correct (VERIFIED) (n=10): calls C 17 vs N 29 (59% of N); input tokens C 774121 vs N 1052377 (74%); result bytes C 31743 vs N 18509 (172%)
- S9 all 12 (n=12): calls C 19 vs N 36 (53% of N); input tokens C 886189 vs N 1331443 (67%); result bytes C 35935 vs N 25992 (138%)

Zero-tool-call runs: none
Non-zero exit or timed out: none
C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1762 vs N 707
- H-L2: calls C 1 vs N 1; bytes C 982 vs N 64
- H-X1: calls C 3 vs N 3; bytes C 4263 vs N 2952
- H-M1: calls C 3 vs N 1; bytes C 5846 vs N 185
- H-L3: calls C 1 vs N 1; bytes C 724 vs N 304
- H-X2: calls C 4 vs N 2; bytes C 3415 vs N 6109

Locate tasks bytes C/N: H-L1 C 1762 / N 707; H-L2 C 982 / N 64; H-L3 C 724 / N 304

Arm C devx errors and non-devx tool use:
- H-X1: devx error `/bin/zsh -lc 'devx read method "sign" "limitinf" --session <SESSION-F2> --agent codex'`
- H-X2: devx error `/bin/zsh -lc "devx callers 'RipgrepLocator.Locate' --session <SESSION-F3> --agent codex"`
- H-X2: devx error `/bin/zsh -lc "devx callers 'DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate' --session <SESSION-F3> --agent codex"`

## Verified results (blinded rescore, joined with out-of-repo key)

Files: results/series11/rescore-blind11.csv (blind ids) and rescore11.csv (task,arm,verdict,reason). Rescorer used 8 tool calls.

Arm C VERIFIED correct: 12/12 (automated 12/12); without H-M1: 11/11
Arm N VERIFIED correct: 11/12 (automated 12/12); without H-M1: 11/11
Incorrect verdicts: A08 (H-M1, arm N)
Agreement automated vs blinded: 23/24 answers; the 1 disagreements are exactly the incorrect verdicts above (automated scorer marked them correct).

- S11 both-correct (VERIFIED) (n=11): calls C 17 vs N 19 (89% of N); input tokens C 405640 vs N 422764 (96%); result bytes C 22448 vs N 76422 (29%)
- S11 all 12 (VERIFIED) (n=12): calls C 20 vs N 20 (100% of N); input tokens C 465035 vs N 450411 (103%); result bytes C 28294 vs N 76607 (37%)

Series 5-9 on verified verdicts:
- S5 both-correct (VERIFIED) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
- S5 all 12 (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
- S6 both-correct (VERIFIED) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S7 both-correct (VERIFIED) (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S7 all 12 (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S8 both-correct (VERIFIED) (n=11): calls C 16 vs N 18 (89% of N); input tokens C 539293 vs N 537944 (100%); result bytes C 22630 vs N 14550 (156%)
- S8 all 12 (n=12): calls C 18 vs N 19 (95% of N); input tokens C 599063 vs N 574979 (104%); result bytes C 23553 vs N 14734 (160%)
- S9 both-correct (VERIFIED) (n=10): calls C 17 vs N 29 (59% of N); input tokens C 774121 vs N 1052377 (74%); result bytes C 31743 vs N 18509 (172%)
- S9 all 12 (n=12): calls C 19 vs N 36 (53% of N); input tokens C 886189 vs N 1331443 (67%); result bytes C 35935 vs N 25992 (138%)

Rulings: maintainer upheld all three H-M1 incorrect verdicts (series 10: A05, A13; series 11: A08), each naming C89CodePrinter where the fixed reference is CodePrinter at codeprinter.py:53, consistent with series 8. H-M1's wording ("Name that class") is loose: it has cost answers in series 8, 10 and 11 across three models, so future task sets must phrase the target unambiguously. Correctness is shown with and without H-M1 above.

Rescorer's immaterial deviations: A22 gave caller lines 96/102 vs derivation 103/109 (question did not ask lines) and A24 gave the method-start line for both messages (both immaterial, rated correct).
