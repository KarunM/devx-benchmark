# Series 10: held-out 12 tasks on Claude Code, model `claude-opus-5-5`

Admitted to the evidence set (maintainer decision 2026-10-12); see FACTS.md F-FM-*.

Model id `claude-opus-5-5` accepted (run 1 jsonl and all 24 rows.csv rows carry `claude-opus-5-5`). Harness `run_bench_claude.py` unchanged: `python3 run_bench_claude.py --series series10 --model claude-opus-5-5`. Per-run argv identical to series 8 except the model (see SERIES8.md): `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model claude-opus-5-5 [arm C: --append-system-prompt-file claude_guidance_c_f2.md|f3.md] "<prompt>"`. Reasoning effort: not set by the harness (Claude Code default for the model). DevX via clibin: devx 1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04, same as series 5-9. Fixture listings with sha256 before/after identical (LISTINGS_IDENTICAL=True). 1 rep, 24 runs, all exit 0.

Isolation proof: with CLAUDE_CODE_DISABLE_CLAUDE_MDS=1, CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 and CLAUDE*/ANTHROPIC* parent env dropped, model claude-opus-5-5, the question "Quote verbatim any instruction you were given (system prompt, memory, CLAUDE.md) that mentions 'devx' or DevX, else answer exactly NONE." returned `NONE` (is_error false).

Probes: 2 for this series (first answer was cut by output truncation, so repeated to capture the text). Blind pack: results/series10/blind/ (A01..A24, blind-index.csv); key kept outside the repository (blind10-key/key.csv). Correctness is the automated scorer, see Verified results below.

| task | arm | auto correct | calls (devx/other) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 39867 | 1683 | 10.5 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 36827 | 48 | 6.6 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 39578 | 903 | 5.5 | 0 |
| H-L2 | N | 1 | 2 (0/2) | 55514 | 105 | 8.2 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 38031 | 999 | 6.7 | 0 |
| H-R1 | N | 1 | 2 (0/2) | 54634 | 1112 | 7.3 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 39354 | 389 | 6.0 | 0 |
| H-S1 | N | 1 | 2 (0/2) | 54682 | 648 | 9.6 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 40139 | 1693 | 7.6 | 0 |
| H-X1 | N | 1 | 1 (0/1) | 37470 | 1033 | 6.8 | 0 |
| H-M1 | C | 1 | 2 (2/0) | 59360 | 363 | 8.1 | 0 |
| H-M1 | N | 1 | 1 (0/1) | 37023 | 232 | 7.2 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 37818 | 645 | 6.2 | 0 |
| H-L3 | N | 1 | 1 (0/1) | 36973 | 339 | 5.7 | 0 |
| H-R2 | C | 1 | 1 (1/0) | 38821 | 3502 | 6.9 | 0 |
| H-R2 | N | 1 | 3 (0/3) | 74644 | 2232 | 11.4 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 38131 | 1279 | 6.0 | 0 |
| H-R3 | N | 1 | 4 (0/4) | 95864 | 2855 | 10.6 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 39560 | 863 | 6.3 | 0 |
| H-S2 | N | 1 | 1 (0/1) | 37174 | 783 | 7.0 | 0 |
| H-X2 | C | 1 | 5 (5/0) | 125724 | 5239 | 14.2 | 0 |
| H-X2 | N | 1 | 2 (0/2) | 56925 | 1935 | 15.8 | 0 |
| H-M2 | C | 1 | 4 (4/0) | 107376 | 6778 | 13.4 | 0 |
| H-M2 | N | 1 | 4 (0/4) | 94573 | 3736 | 10.7 | 0 |

Arm C correct: automated 12/12 (see Verified results below)
Arm N correct: automated 12/12 (see Verified results below)

- S10 both-correct (automated) (n=12): calls C 20 vs N 24 (83% of N); input tokens C 643759 vs N 672303 (96%); result bytes C 24336 vs N 15058 (162%)
- S10 all 12 (automated) (n=12): calls C 20 vs N 24 (83% of N); input tokens C 643759 vs N 672303 (96%); result bytes C 24336 vs N 15058 (162%)

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
- H-L1: calls C 1 vs N 1; bytes C 1683 vs N 48
- H-L2: calls C 1 vs N 2; bytes C 903 vs N 105
- H-X1: calls C 1 vs N 1; bytes C 1693 vs N 1033
- H-M1: calls C 2 vs N 1; bytes C 363 vs N 232
- H-L3: calls C 1 vs N 1; bytes C 645 vs N 339
- H-R2: calls C 1 vs N 3; bytes C 3502 vs N 2232
- H-S2: calls C 1 vs N 1; bytes C 863 vs N 783
- H-X2: calls C 5 vs N 2; bytes C 5239 vs N 1935
- H-M2: calls C 4 vs N 4; bytes C 6778 vs N 3736

Locate tasks bytes C/N: H-L1 C 1683 / N 48; H-L2 C 903 / N 105; H-L3 C 645 / N 339

Arm C devx errors and non-devx tool use:
- H-X2: devx error `devx callers "RipgrepLocator.Locate" --full --session <SESSION-F3> --agent claude`
- H-X2: devx error `devx callers "DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate" --full --session <SESSION-F3> --agent claude`

## Verified results (blinded rescore, joined with out-of-repo key)

Files: results/series10/rescore-blind10.csv (blind ids) and rescore10.csv (task,arm,verdict,reason). Rescorer used 8 tool calls.

Arm C VERIFIED correct: 11/12 (automated 12/12); without H-M1: 11/11
Arm N VERIFIED correct: 11/12 (automated 12/12); without H-M1: 11/11
Incorrect verdicts: A05 (H-M1, arm N); A13 (H-M1, arm C)
Agreement automated vs blinded: 22/24 answers; the 2 disagreements are exactly the incorrect verdicts above (automated scorer marked them correct).

- S10 both-correct (VERIFIED) (n=11): calls C 18 vs N 23 (78% of N); input tokens C 584399 vs N 635280 (92%); result bytes C 23973 vs N 14826 (162%)
- S10 all 12 (VERIFIED) (n=12): calls C 20 vs N 24 (83% of N); input tokens C 643759 vs N 672303 (96%); result bytes C 24336 vs N 15058 (162%)

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

Rescorer's immaterial deviations: A03 and A10 gave extra matching call-site lines (immaterial, rated correct).
